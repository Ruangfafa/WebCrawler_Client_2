from dotenv import load_dotenv
import os

# 自动从 .env 文件加载变量
load_dotenv()

# 读取数据库配置项
DB_HOST=os.getenv("DB_HOST")
DB_PORT=int(os.getenv("DB_PORT"))
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_ssl_disabled=os.getenv("DB_ssl_disabled")=="True"

# 读取Log配置项
LOG_PRINT=os.getenv("LOG_PRINT")=="True"