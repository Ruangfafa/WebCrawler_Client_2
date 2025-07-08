import mysql.connector
from app.common.config_loader import LOG_PRINT
from mysql.connector import Error
from app.service.log import log
from app.common.constants import LogMessageCons, LogSourceCons

def get_connection(host, port, user, password, ssl_disabled):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            ssl_disabled=ssl_disabled
        )
        if connection.is_connected():
            log(LogMessageCons.DB_LOGIN_SUCCESS, error=None, source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
            return connection
    except Error as e:
        log(LogMessageCons.DB_LOGIN_FAIL, error=e, source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
        return None