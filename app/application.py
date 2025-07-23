import time

from app.common.constants import DatabaseServicePy
from app.common.config_loader import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_SSL_DISABLED
from app.service.chrome_driver_service import init_driver
from app.service.crawlers import seller_tag_crawler, product_tag_crawler, product_crawler, comment_crawler
from app.service.database_service import get_connection, get_state, set_state, remove_url, get_a_url
import app.service.crawlers.seller_crawler as seller_crawler

# 调用数据库连接
import time

# 连接数据库和浏览器
conn = get_connection(DB_HOST,DB_PORT,DB_USER,DB_PASSWORD,DB_SSL_DISABLED)
driver = init_driver()

while (state := get_state(conn, DB_USER, DatabaseServicePy.STATE_STATE)) != -1:

    while state == 1 and get_state(conn, DB_USER, DatabaseServicePy.STATE_LOCK) == 0:
        if (taskUrl := get_a_url(conn, DB_USER)) is None:
            set_state(conn, DB_USER, DatabaseServicePy.STATE_STATE, 0)
            break
        start_time = time.time()
        if seller_crawler.craw(conn, driver, taskUrl[1]):
            remove_url(conn, DB_USER, taskUrl[0])
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)

    while state == 2 and get_state(conn, DB_USER, DatabaseServicePy.STATE_LOCK) == 0:
        if (taskUrl := get_a_url(conn, DB_USER)) is None:
            set_state(conn, DB_USER, DatabaseServicePy.STATE_STATE, 0)
            break
        start_time = time.time()
        if seller_tag_crawler.craw(conn, driver, taskUrl[1]):
            remove_url(conn, DB_USER, taskUrl[0])
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)

    while state == 3 and get_state(conn, DB_USER, DatabaseServicePy.STATE_LOCK) == 0:
        if (taskUrl := get_a_url(conn, DB_USER)) is None:
            set_state(conn, DB_USER, DatabaseServicePy.STATE_STATE, 0)
            break
        start_time = time.time()
        if product_tag_crawler.craw(conn, driver, taskUrl[1]):
            remove_url(conn, DB_USER, taskUrl[0])
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)

    while state == 5 and get_state(conn, DB_USER, DatabaseServicePy.STATE_LOCK) == 0:
        if (taskUrl := get_a_url(conn, DB_USER)) is None:
            set_state(conn, DB_USER, DatabaseServicePy.STATE_STATE, 0)
            break
        start_time = time.time()
        if product_crawler.craw(conn, driver, taskUrl[1]):
            remove_url(conn, DB_USER, taskUrl[0])
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)

    while state == 6 and get_state(conn, DB_USER, DatabaseServicePy.STATE_LOCK) == 0:
        if (taskUrl := get_a_url(conn, DB_USER)) is None:
            set_state(conn, DB_USER, DatabaseServicePy.STATE_STATE, 0)
            break
        start_time = time.time()
        if comment_crawler.craw(conn, driver, taskUrl[1]):
            remove_url(conn, DB_USER, taskUrl[0])
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)

    # 主循环每轮停 3 秒，避免高频轮询数据库
    time.sleep(3)
