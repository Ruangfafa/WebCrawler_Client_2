from app.service.database_service import get_connection
from app.common.config_loader import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_ssl_disabled

# 调用数据库连接
conn = get_connection(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_ssl_disabled)
