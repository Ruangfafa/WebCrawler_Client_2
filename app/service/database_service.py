import mysql.connector
from app.common.config_loader import LOG_PRINT
from mysql.connector import Error, MySQLConnection
from app.service.log import log
from app.common.constants import LogMessageCons, LogSourceCons, DatabaseServicePy

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
            log(LogMessageCons.DB_LOGIN_SUCCESS, source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
            return connection
    except Error as e:
        log(LogMessageCons.DB_LOGIN_FAIL, source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT, error=e)
        return None

def get_status(conn: MySQLConnection, database: str, key: str):
    try:
        conn.commit()
        cursor = conn.cursor()
        # 格式化插入 database，其他保持参数化
        sql_template = DatabaseServicePy.SQL_CLIENTSTATUS_SELECT
        sql = sql_template % database  # 安全格式化 database 名称
        cursor.execute(sql, (key,))    # 参数化 key 值

        row = cursor.fetchone()
        if row:
            value = int(row[0])
            log(message=LogMessageCons.DB_CLIENT_GETSTATE_SUCCESS % (database, key, value), source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
            return value
        else:
            log(message=LogMessageCons.DB_CLIENT_GETSTATE_NOTFOUND % (database, key), source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
            return None

    except Error as e:
        log(message=LogMessageCons.DB_CLIENT_GETSTATE_FAIL % (database, key), error=e, source=LogSourceCons.DATABASE_SERVICE, doPrint=LOG_PRINT)
        return None