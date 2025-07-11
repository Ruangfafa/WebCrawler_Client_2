import os


class LogMessageCons:
    DB_LOGIN_SUCCESS = "✔️数据库连接成功"
    DB_LOGIN_FAIL = "❌数据库连接失败"
    DB_CLIENT_GETSTATE_SUCCESS = "✔️成功读取状态：%s.State - %s = %d"
    DB_CLIENT_GETSTATE_NOTFOUND = "⚠️未找到状态：%s.State - key = %s"
    DB_CLIENT_GETSTATE_FAIL = "❌读取状态失败：%s.State - key = %s"
    DB_CLIENT_SETSTATE_SUCCESS = "✔️成功设置状态：%s.State - %s = %d"
    DB_CLIENT_SETSTATE_FAIL = "❌设置状态失败：%s.State - %s = %d"
    DB_GET_URL_FAIL = "❌获取URL失败：%s.Task"
    DB_REMOVE_URL_SUCCESS = "✔️成功删除 URL：%s.Task - id = %d"
    DB_REMOVE_URL_FAIL = "❌删除 URL 失败：%s.Task - id = %d"
    DB_SERVER_INSERT_SUCCESS = "✔️成功插入 Seller 表记录：Server.%s"
    DB_SERVER_INSERT_FAIL = "❌插入 Seller 表记录失败：Server.%s"

    CD_INIT_FAIL = "❌Chrome 驱动初始化失败"
    CD_INIT_START = "⚠️正在初始化 Chrome 驱动..."
    CD_INIT_SUCCESS = "✔️Chrome 驱动初始化完成"
    CD_USERDATA_PATH = "⚠️用户数据路径：%s"
    CD_GETURL_SUCCESS = "✔️当前网址获取成功：%s"
    CD_GETURL_FAIL = "❌获取当前网址失败"
    CD_MOVE_FAIL = "❌未找到元素：%s"
    CD_FIND_ELEMENT_SUCCESS = "✔️成功找到元素"
    CD_FIND_ELEMENT_FAIL = "❌未找到元素：%s"
    CD_FIND_ELEMENTS_SUCCESS = "✔️成功找到元素列表"
    CD_FIND_ELEMENTS_FAIL = "❌未找到元素列表：%s"
    CD_GET_ATTRIBUTE_SUCCESS = "✔️成功找到属性"
    CD_GET_ATTRIBUTE_FAIL = "❌未找到属性"

    AP_SAFE_CONTINUE_SUCCESS = "✔️无异常拦截"
    AP_SAFE_CONTINUE_WAIT = "⚠️异常拦截，等待手动恢复中..."

    AP_PERSIST_FIND_ELEMENT_SUCCESS = "✔️成功找到元素：%s"
    AP_PERSIST_FIND_ELEMENT_TRY = "⚠️暂未找到元素，重试中..."
    AP_PERSIST_FIND_ELEMENT_FAIL = "❌未找到元素"
    AP_PERSIST_FIND_ELEMENTS_SUCCESS = "✔️成功找到元素列表：%s"
    AP_PERSIST_FIND_ELEMENTS_TRY = "⚠️暂未找到元素列表，重试中..."
    AP_PERSIST_FIND_ELEMENTS_FAIL = "❌未找到元素列表"
    AP_PERSIST_GET_ATTRIBUTE_SUCCESS = "✔️成功找到属性：%s"
    AP_PERSIST_GET_ATTRIBUTE_TRY = "⚠️暂未找到属性，重试中..."
    AP_PERSIST_GET_ATTRIBUTE_FAIL = "❌未找到属性"


class LogSourceCons:
     DATABASE_SERVICE = "app/service/database_service.py"
     CHROME_DRIVER_SERVICE = "app/service/chrome_driver_service.py"
     ABNORMAL_PROCESSING_SERVICE = "app/service/abnormal_processing_service.py"

class LogPy:
    TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_FORMAT = "[{timestamp}] [{source}] {message}"
    LOG_FORMAT_WITH_ERROR = "[{timestamp}] [{source}] {message} | ERROR: {error}"

class DatabaseServicePy:
    SQL_CLIENTSTATUS_SELECT = "SELECT value FROM %s.State WHERE `key` = %%s LIMIT 1"
    SQL_TASK_SELECT_FIRST = "SELECT id, url FROM %s.Task ORDER BY id ASC LIMIT 1"
    SQL_TASK_DELETE_BY_ID = "DELETE FROM %s.Task WHERE id = %%s"
    SQL_CLIENTSTATUS_UPDATE = "UPDATE %s.State SET value = %%s WHERE `key` = %%s"
    SQL_DATA_INSERT = "INSERT INTO Server.%s (%s) VALUES (%s)"
    SQL_COLUMNS_JOIN = ", ".join  # 用于列名拼接
    SQL_PLACEHOLDER_JOIN = lambda count: ", ".join(["%s"] * count)

    STATE_STATE = "state"
    STATE_LOCK = "lock"
    FORMAT_BLANK = ""
    FORMAT_UNDERLINE = "_"

class ChromeDriverServicePy:
    # 路径配置
    BASE_DIR = os.path.abspath(os.path.join(__file__, "../../.."))
    CHROME_DIR = os.path.join(BASE_DIR, "resources", "chrome_chromedriver_137.0.7151.119")
    CHROME_PATH = os.path.join(CHROME_DIR, "chrome.exe")
    DRIVER_PATH = os.path.join(CHROME_DIR, "chromedriver.exe")

    JS_READYSTATE_GET = "return document.readyState"
    JS_READYSTATE = "complete"
    JS_GET_TEXT = "return arguments[0].textContent.trim();"

    # 浏览器参数配置
    WINDOW_SIZE = "--window-size=1920,1080"
    USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    EXCLUDE_SWITCHES = ["enable-automation"]
    DISABLE_FEATURES = "--disable-blink-features=AutomationControlled"
    NO_SANDBOX = "--no-sandbox"
    DISABLE_DEV_SHM = "--disable-dev-shm-usage"
    DETACH = True
    EXPERIMENTAL_OPTION_DETACH = "detach"
    EXPERIMENTAL_OPTION_EXCLUDE_SWITCHES = "excludeSwitches"
    HEADLESS_ARG = "--headless=new"

    @staticmethod
    def get_user_data_arg(USER_FILE: str):
        user_dir = os.path.join(ChromeDriverServicePy.CHROME_DIR, USER_FILE)
        return f"--user-data-dir={user_dir}"


class SellerCrawlerPy:
    XPATH_NAME = "//a[contains(@class, 'slogo-shopname')]/strong"
    XPATH_LOCATION_TRIANGLE = "//i[contains(@class,'icon-triangle')]"
    XPATH_LOCATION = "//li[contains(@class,'locus')]//div[contains(@class,'right')]"
    XPATH_SCORE_ELEMENTS = "//span[contains(@class, 'shopdsr-score-con')]"

    BLANK_DATA = "?"
    NO_DATA = "N/A"

class SellerTagCrawlerPy:
    XPATH_C_PROPS = "//div[contains(@class, 'tshop-pbsm-shop-nav-ch')]//ul[contains(@class, 'J_TAllCatsTree') and contains(@class, 'cats-tree')]/li[position() > 1]"
    XPATH_C_TAG = "./h4/a"
    XPATH_CC_PROPS = "./div//li"
    XPATH_CC_TAG = "./h4/a"
    XPATH_P_PROPS = "//div[contains(@class, 'propAttrs')]//div[contains(@class, 'attr') and contains(@class, 'J_TProp')]"
    XPATH_P_PROP_KEY = ".//div[contains(@class, 'attrKey')]"
    XPATH_P_TAGS = ".//div[contains(@class, 'attrValues')]//ul[contains(@class, 'av-collapse')]//li//a"

    BLANK_DATA = "?"
    NO_DATA = "N/A"
    ALL_PRODUCT = "所有分类"
    CATEGORY_ALL_PREFIX = "a_:_xxxxx"
    REGEX_CATEGORY_C = r'category-(\d+)'
    CATEGORY_C_PREFIX = "c_:_%s"
    CATEGORY_CC_PREFIX_TAG = "%s_:_%s"
    REGEX_CATEGORY_P = r"pv=([^&]+)"
    CATEGORY_P_PREFIX = "p_:_%s"
    CATEGORY_P_PREFIX_TAG = "%s_:_%s"
    ATTRIBUTE_HREF = "href"
