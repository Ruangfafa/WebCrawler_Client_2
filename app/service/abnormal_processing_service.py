import time

from selenium.webdriver.common.by import By

from app.common.config_loader import PAGE_LOAD_TIMEOUT, URLS, XPATHS, LOG_PRINT
from app.common.constants import LogMessageCons, LogSourceCons
from app.service.chrome_driver_service import get_url, find_element, if_ready_state, find_elements, get_attribute
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
            if safe: safe_continue(driver)
            time.sleep(0.25)
            return True
    return False

def safe_continue(driver, log_print=LOG_PRINT):
    """
    在进入操作流程前进行验证码拦截检查。
    若命中指定 URL 或 XPath 特征，则进入等待循环。
    否则立即返回继续执行。
    """
    # 检查 URL
    abnormal = False
    while (
            any(bypass_url in get_url(driver) for bypass_url in URLS) or
            any(find_element(driver, By.XPATH, xpath, False) for xpath in XPATHS)
    ):
        abnormal = True
        log(LogMessageCons.AP_SAFE_CONTINUE_WAIT, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, log_print)
        time.sleep(1)
    log(LogMessageCons.AP_SAFE_CONTINUE_SUCCESS, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, log_print)
    if abnormal: wait_load(driver, False)

def safe_find_element(driver, by, value, log_print=LOG_PRINT):
    safe_continue(driver)
    return find_element(driver, by, value, log_print)

def persist_find_element(driver, by, value, duration=0.5, retry=10, safe=True):
    for attempt in range(retry):
        if safe:
            element = safe_find_element(driver, by, value, False)
        else:
            element = find_element(driver, by, value, False)
        if element:
            log(LogMessageCons.AP_PERSIST_FIND_ELEMENT_SUCCESS % element, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
            return element
        time.sleep(duration)
        log(LogMessageCons.AP_PERSIST_FIND_ELEMENT_TRY, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    log(LogMessageCons.AP_PERSIST_FIND_ELEMENT_FAIL, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return None  # 最终未找到

def safe_find_elements(driver, by, value, log_print=LOG_PRINT):
    safe_continue(driver)
    return find_elements(driver, by, value, log_print)

def persist_find_elements(driver, by, value, duration=0.5, retry=10, safe=True):
    for attempt in range(retry):
        if safe:
            elements = safe_find_elements(driver, by, value, False)
        else:
            elements = find_elements(driver, by, value, False)
        if elements:
            log(LogMessageCons.AP_PERSIST_FIND_ELEMENTS_SUCCESS % elements, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
            return elements
        time.sleep(duration)
        log(LogMessageCons.AP_PERSIST_FIND_ELEMENTS_TRY, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    log(LogMessageCons.AP_PERSIST_FIND_ELEMENTS_FAIL, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return []  # 最终未找到

def safe_get_attribute(driver, element, value, log_print=LOG_PRINT):
    safe_continue(driver)
    return get_attribute(element, value, log_print)

def persist_get_attribute(driver, element, value, duration=0.5, retry=10, safe=True):
    for attempt in range(retry):
        if safe:
            attribute = safe_get_attribute(driver, element, value, False)
        else:
            attribute = get_attribute(element, value, False)
        if attribute:
            log(LogMessageCons.AP_PERSIST_GET_ATTRIBUTE_SUCCESS % attribute, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
            return attribute
        time.sleep(duration)
        log(LogMessageCons.AP_PERSIST_GET_ATTRIBUTE_TRY, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    log(LogMessageCons.CD_GET_ATTRIBUTE_FAIL, LogSourceCons.ABNORMAL_PROCESSING_SERVICE, LOG_PRINT)
    return None

