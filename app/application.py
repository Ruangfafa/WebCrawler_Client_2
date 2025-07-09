import time

from app.common.constants import DatabaseServicePy
from app.common.config_loader import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_ssl_disabled
from app.service.chrome_driver_service import init_driver
from app.service.database_service import get_connection, get_status

# 调用数据库连接
conn = get_connection(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_ssl_disabled)
driver = init_driver()
while (state := get_status(conn, DB_USER, DatabaseServicePy.STATE_STATE)) != -1:
    match state:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
    time.sleep(5)