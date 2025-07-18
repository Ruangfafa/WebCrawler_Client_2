from selenium.common import JavascriptException
from selenium.webdriver import ActionChains
import undetected_chromedriver as uc


from app.common.config_loader import HEADLESS, LOG_PRINT, USER_FILE
from app.common.constants import ChromeDriverServicePy, LogMessageCons, LogSourceCons
from app.service.log import log


def init_driver() -> uc.Chrome:
    try:
        log(LogMessageCons.CD_INIT_START, LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT)

        options = uc.ChromeOptions()
        options.add_argument(ChromeDriverServicePy.WINDOW_SIZE)
        options.add_argument(ChromeDriverServicePy.get_user_data_arg(USER_FILE))
        options.add_argument(ChromeDriverServicePy.USER_AGENT)
        options.add_argument(f"--disable-blink-features={ChromeDriverServicePy.DISABLE_FEATURES}")
        options.add_argument(ChromeDriverServicePy.NO_SANDBOX)
        options.add_argument(ChromeDriverServicePy.DISABLE_DEV_SHM)
        if HEADLESS:
            options.add_argument(ChromeDriverServicePy.HEADLESS_ARG)

        log(LogMessageCons.CD_USERDATA_PATH % ChromeDriverServicePy.get_user_data_arg(USER_FILE), LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT)

        # 用 uc.Chrome() 替代原本 webdriver.Chrome(service=..., options=...)
        driver = uc.Chrome(options=options, use_subprocess=True)  # 可指定 Chrome 主版本号（自动适配驱动）
        log(LogMessageCons.CD_INIT_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT)
        return driver
    except Exception as e:
        log(LogMessageCons.CD_INIT_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT, e)
        raise e

def get_url(driver):
    try:
        url = driver.current_url
        log(LogMessageCons.CD_GETURL_SUCCESS % url, LogSourceCons.CHROME_DRIVER_SERVICE, False)
        return url
    except Exception as e:
        log(LogMessageCons.CD_GETURL_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT, e)
        return None

def find_element(driver, by, xpath, log_print=LOG_PRINT):
    try:
        element = driver.find_element(by, xpath)
        log(LogMessageCons.CD_FIND_ELEMENT_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, log_print)
        return element
    except Exception as e:
        log(LogMessageCons.CD_FIND_ELEMENT_FAIL % xpath, LogSourceCons.CHROME_DRIVER_SERVICE, log_print, e)
        return None

def find_elements(driver, by, value, log_print=LOG_PRINT):
    try:
        elements = driver.find_elements(by, value)
        log(LogMessageCons.CD_FIND_ELEMENTS_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, log_print)
        return elements
    except Exception as e:
        log(LogMessageCons.CD_FIND_ELEMENTS_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, log_print, e)
        return None

def get_attribute(element, value, log_print=LOG_PRINT):
    try:
        attribute = element.get_attribute(value)
        log(LogMessageCons.CD_GET_ATTRIBUTE_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, log_print)
        return attribute
    except Exception as e:
        log(LogMessageCons.CD_GET_ATTRIBUTE_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, log_print, e)
        return None

def if_ready_state(driver):
    try:
        if driver.execute_script(ChromeDriverServicePy.JS_READYSTATE_GET) == ChromeDriverServicePy.JS_READYSTATE: return True
        return False
    except JavascriptException:
        pass  # 某些 iframe 或异步加载可能引发错误，忽略重试

def move_to_element(driver, item, click=False):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(item)
        if click:
            actions.click()
        actions.perform()
        return True
    except Exception as e:
        log(LogMessageCons.CD_MOVE_FAIL % item, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT, e)
        return False

def move_by_offset(driver, offset_x, offset_y, click=False):
    actions = ActionChains(driver)
    actions.move_by_offset(offset_x, offset_y)
    if click: actions.click()
    actions.perform()

def get_text(driver, source_element):
    try:
        text = driver.execute_script(ChromeDriverServicePy.JS_GET_TEXT, source_element).strip()
    except JavascriptException:
        text = None
    return text

def scroll_bottom(driver, source_element):
    try:
        driver.execute_script(ChromeDriverServicePy.JS_SCROLL_BOTTOM, source_element)
        log(LogMessageCons.CD_SCROLL_BOTTOM_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT)
    except Exception as e:
        log(LogMessageCons.CD_SCROLL_BOTTOM_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT, e)

def scroll_top(driver, source_element):
    try:
        driver.execute_script(ChromeDriverServicePy.JS_SCROLL_TOP, source_element)
        log(LogMessageCons.CD_SCROLL_TOP_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT)
    except Exception as e:
        log(LogMessageCons.CD_SCROLL_TOP_FAIL, LogSourceCons.CHROME_DRIVER_SERVICE, LOG_PRINT, e)
