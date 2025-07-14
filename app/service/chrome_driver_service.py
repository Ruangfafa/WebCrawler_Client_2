import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from app.common.config_loader import HEADLESS, LOG_PRINT, USER_FILE
from app.common.constants import ChromeDriverServicePy, LogMessageCons, LogSourceCons
from app.service.log import log


def init_driver() -> webdriver.Chrome:
    try:
        log(LogMessageCons.CD_INIT_START, LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT)
        # 参数配置
        options = Options()
        options.add_argument(ChromeDriverServicePy.WINDOW_SIZE)
        options.add_argument(ChromeDriverServicePy.get_user_data_arg(USER_FILE))
        options.add_argument(ChromeDriverServicePy.USER_AGENT)
        options.add_experimental_option(ChromeDriverServicePy.EXPERIMENTAL_OPTION_EXCLUDE_SWITCHES, ChromeDriverServicePy.EXCLUDE_SWITCHES)
        options.add_argument(ChromeDriverServicePy.DISABLE_FEATURES)
        options.add_argument(ChromeDriverServicePy.NO_SANDBOX)
        options.add_argument(ChromeDriverServicePy.DISABLE_DEV_SHM)
        options.add_experimental_option(ChromeDriverServicePy.EXPERIMENTAL_OPTION_DETACH, ChromeDriverServicePy.DETACH)
        if HEADLESS: options.add_argument(ChromeDriverServicePy.HEADLESS_ARG)  # 启用无头模式（可选）
        log(LogMessageCons.CD_USERDATA_PATH % ChromeDriverServicePy.get_user_data_arg(USER_FILE), LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT)
        service = Service(ChromeDriverServicePy.DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        log(LogMessageCons.CD_INIT_SUCCESS, LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT)
        return driver
    except Exception as e:
        log(message=LogMessageCons.CD_INIT_FAIL % str(e), source=LogSourceCons.CHROME_DRIVER_SERVICE, doPrint=LOG_PRINT, error=e)
        raise e