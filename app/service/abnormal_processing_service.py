import time

from selenium.webdriver.common.by import By

from app.common.config_loader import LOG_PRINT, PAGE_LOAD_TIMEOUT, URLS, XPATHS
from app.common.constants import LogMessageCons, LogSourceCons
from app.service.chrome_driver_service import get_url, find_element, if_ready_state, find_elements
from app.service.log import log

def wait_load(driver, safe=True):
    """
    等待页面加载完成。
    - 初始等待1秒
    - 通过 document.readyState 判断页面加载状态
    - 超时返回 False，否则返回 True
    """
    time.sleep(1)  # 初始等待
    start_time = time.time()
    while time.time() - start_time < PAGE_LOAD_TIMEOUT:
        if if_ready_state(driver):
            if safe:
                safe_continue(driver)
            return True
        time.sleep(0.25)
    return False

def safe_continue(driver):
    """
    在进入操作流程前进行验证码拦截检查。
    若命中指定 URL 或 XPath 特征，则进入等待循环。
    否则立即返回继续执行。
    """
    current_url = get_url(driver)
    # 检查 URL
    if any(bypass_url in current_url for bypass_url in URLS):
        log(LogMessageCons.AP_HIT_URL % current_url, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
        while True:
            time.sleep(0.25)
    # 检查 XPath
    for xpath in XPATHS:
        try:
            if find_element(driver, By.XPATH, xpath):
                log(LogMessageCons.AP_HIT_XPATH % xpath, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
                while True:
                    time.sleep(0.25)
        except Exception:
            continue  # 忽略未命中

    wait_load(driver, False)

def safe_find_element(driver, by, value):
    """
    封装 driver.find_element，附带验证码路径识别机制。
    如果当前 URL 或 XPath 命中验证码白名单，则进入等待循环。
    """
    safe_continue(driver)
    # 默认行为：正常查找
    element = find_element(driver, by, value)
    if element: log(LogMessageCons.AP_FIND_SUCCESS % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    else: log(LogMessageCons.AP_FIND_FAIL % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return element

def persist_find_element(driver, by, value, duration=0.5, retry=10, safe=True):
    """
    尝试重复查找某个元素，最多 retry 次，每次间隔 duration 秒。
    参数：
        safe: 是否启用 safe_find_element 模式（会自动验证码拦截）
    返回：
        成功返回 WebElement，失败返回 None
    """
    for attempt in range(retry):
        try:
            if safe:
                elem = safe_find_element(driver, by, value)
                if elem == None: raise Exception("Element not found")
            else:
                elem = find_element(driver, by, value)
                if elem == None: raise Exception("Element not found")
            log(LogMessageCons.AP_FIND_SUCCESS % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
            return elem  # 找到了就直接返回
        except Exception:
            time.sleep(duration)
    log(LogMessageCons.AP_FIND_FAIL % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return None  # 最终未找到

def persist_find_elements(driver, by, value, duration=0.5, retry=10, safe=True):
    """
    尝试重复查找多个元素（elements 列表），最多 retry 次，每次间隔 duration 秒。
    参数：
        safe: 是否启用 safe_continue 拦截机制（不对 elements 逐一验证）
    返回：
        成功返回 WebElement 列表，失败返回空列表
    """
    for attempt in range(retry):
        try:
            if safe:
                safe_continue(driver)
            elements = find_elements(driver, by, value)
            if elements:
                log(LogMessageCons.AP_FIND_SUCCESS % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
                return elements
        except Exception:
            pass
        time.sleep(duration)

    log(LogMessageCons.AP_FIND_FAIL % value, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return []  # 最终未找到