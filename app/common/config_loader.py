from datetime import timezone, timedelta

from dotenv import load_dotenv
import os

# 自动从 .env 文件加载变量
load_dotenv()

# 读取数据库配置项
DB_HOST=os.getenv("DB_HOST")
DB_PORT=int(os.getenv("DB_PORT"))
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_SSL_DISABLED=os.getenv("DB_SSL_DISABLED")=="True"

# 读取Log配置项
LOG_PRINT=os.getenv("LOG_PRINT")=="True"

# 读取Chrome配置项
HEADLESS=os.getenv("HEADLESS")=="True"
USER_FILE=os.getenv("USER_FILE")

# 读取Properties配置项
TIME_ZONE=timezone(timedelta(hours =int(os.getenv("TIME_ZONE"))))
PAGE_LOAD_TIMEOUT=int(os.getenv("PAGE_LOAD_TIMEOUT"))

# 读取异常处理验证拦截配置（以逗号分隔）
def parse_list(env_key):
    raw = os.getenv(env_key, "")
    return [item.strip() for item in raw.split('_,_') if item.strip()]

URLS = parse_list("URLS")
XPATHS = parse_list("XPATHS")

# CommentCrawler
IN_DATE=int(os.getenv("IN_DATE"))