import os


class LogMessageCons:
    DB_LOGIN_SUCCESS = "✔️数据库连接成功"
    DB_LOGIN_FAIL = "❌数据库连接失败"

    DB_CLIENT_GETSTATE_SUCCESS = "✔️成功读取状态：%s.State - %s = %d"
    DB_CLIENT_GETSTATE_NOTFOUND = "⚠️未找到状态：%s.State - key = %s"
    DB_CLIENT_GETSTATE_FAIL = "❌读取状态失败：%s.State - key = %s"

    CD_INIT_FAIL = "❌Chrome 驱动初始化失败：%s"
    CD_INIT_START = "⚠️正在初始化 Chrome 驱动..."
    CD_INIT_SUCCESS = "✔️Chrome 驱动初始化完成"
    CD_USERDATA_PATH = "⚠️用户数据路径：%s"

class LogSourceCons:
     DATABASE_SERVICE = "app/service/database_service.py"
     CHROME_DRIVER_SERVICE = "app/service/chrome_driver_service.py"

class LogPy:
    TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_FORMAT = "[{timestamp}] [{source}] {message}"
    LOG_FORMAT_WITH_ERROR = "[{timestamp}] [{source}] {message} | ERROR: {error}"

class DatabaseServicePy:
    SQL_CLIENTSTATUS_SELECT = "SELECT value FROM %s.State WHERE `key` = %%s LIMIT 1"

    STATE_STATE = "state"
    STATE_LOCK = "lock"

class ChromeDriverServicePy:
    # 路径配置
    BASE_DIR = os.path.abspath(os.path.join(__file__, "../../.."))
    CHROME_DIR = os.path.join(BASE_DIR, "resources", "chrome_chromedriver_137.0.7151.119")
    CHROME_PATH = os.path.join(CHROME_DIR, "chrome.exe")
    DRIVER_PATH = os.path.join(CHROME_DIR, "chromedriver.exe")

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