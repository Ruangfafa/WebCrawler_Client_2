import re

import mysql.connector

from mysql.connector import Error, MySQLConnection

from app.common.config_loader import LOG_PRINT
from app.common.constants import LogMessageCons, LogSourceCons, DatabaseServicePy
from app.service.log import log

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

def get_state(conn, database, key):
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
            log(LogMessageCons.DB_CLIENT_GETSTATE_SUCCESS % (database, key, value), LogSourceCons.DATABASE_SERVICE, LOG_PRINT)
            return value
        else:
            log(LogMessageCons.DB_CLIENT_GETSTATE_NOTFOUND % (database, key), LogSourceCons.DATABASE_SERVICE, LOG_PRINT)
            return None

    except Error as e:
        log(LogMessageCons.DB_CLIENT_GETSTATE_FAIL % (database, key), LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return None

def set_state(conn: MySQLConnection, database, key, value):
    try:
        cursor = conn.cursor()

        # 尝试更新
        update_sql = DatabaseServicePy.SQL_CLIENTSTATUS_UPDATE % database
        cursor.execute(update_sql, (value, key))

        conn.commit()

        log(LogMessageCons.DB_CLIENT_SETSTATE_SUCCESS % (database, key, value), LogSourceCons.DATABASE_SERVICE, LOG_PRINT)

        return True

    except Error as e:
        log(LogMessageCons.DB_CLIENT_SETSTATE_FAIL % (database, key, value), LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return False

def get_a_url(conn, database):
    try:
        cursor = conn.cursor()
        sql = DatabaseServicePy.SQL_TASK_SELECT_FIRST % database
        cursor.execute(sql)
        row = cursor.fetchone()
        if row: return row  # 返回 (id, url)
        else: return None
    except Error as e:
        log(LogMessageCons.DB_GET_URL_FAIL % database, LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return None

def remove_url(conn, database, task_id):
    try:
        cursor = conn.cursor()
        delete_sql = DatabaseServicePy.SQL_TASK_DELETE_BY_ID % database
        cursor.execute(delete_sql, (task_id,))
        conn.commit()
        log(LogMessageCons.DB_REMOVE_URL_SUCCESS % (database, task_id), LogSourceCons.DATABASE_SERVICE, LOG_PRINT)
        return True
    except Error as e:
        log(LogMessageCons.DB_REMOVE_URL_FAIL % (database, task_id), LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return False

def insert_data(conn, data):
    cursor = conn.cursor()
    table = re.sub(r'(?<!^)(?=[A-Z])', '_', data.__class__.__name__).lower()

    if not isinstance(data, dict):
        data = data.__dict__

    # 转换字段名为 camelCase
    transformed_data = {k: v for k, v in data.items()}

    columns = DatabaseServicePy.SQL_COLUMNS_JOIN(transformed_data.keys())
    placeholders = DatabaseServicePy.SQL_PLACEHOLDER_JOIN(len(transformed_data))
    values = list(transformed_data.values())

    sql = DatabaseServicePy.SQL_DATA_INSERT % (table, columns, placeholders)

    try:
        cursor.execute(sql, values)
        conn.commit()
        log(LogMessageCons.DB_SERVER_INSERT_SUCCESS % table, LogSourceCons.DATABASE_SERVICE, LOG_PRINT)
        return True
    except Exception as e:
        conn.rollback()
        log(LogMessageCons.DB_SERVER_INSERT_FAIL % table, LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return False
    finally:
        cursor.close()

def insert_data_batch(conn, data_list):
    if not data_list:
        return True

    cursor = conn.cursor()
    table = data_list[0].__class__.__name__

    sample = data_list[0].__dict__
    keys = [k for k in sample.keys()]
    columns = DatabaseServicePy.SQL_COLUMNS_JOIN(keys)
    placeholders = DatabaseServicePy.SQL_PLACEHOLDER_JOIN(len(keys))

    sql = DatabaseServicePy.SQL_DATA_INSERT % (table, columns, placeholders)

    values_list = []
    for obj in data_list:
        data = obj.__dict__
        transformed_data = {k: v for k, v in data.items()}
        values_list.append(list(transformed_data.values()))

    try:
        cursor.executemany(sql, values_list)
        conn.commit()
        log(LogMessageCons.DB_SERVER_INSERT_SUCCESS % table, LogSourceCons.DATABASE_SERVICE, LOG_PRINT)
        return True
    except Exception as e:
        conn.rollback()
        log(LogMessageCons.DB_SERVER_INSERT_FAIL % table, LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return False
    finally:
        cursor.close()

def load_whitelist_p_data(conn):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(DatabaseServicePy.SQL_SELLERTAGWHITELIST_SELECT)
        return cursor.fetchall()
    except Exception as e:
        log(LogMessageCons.DB_WHITELISTPTAG_FAIL, LogSourceCons.DATABASE_SERVICE, LOG_PRINT, e)
        return []
    finally:
        cursor.close()