import time
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE, LOG_PRINT, IN_DATE
from app.common.constants import CommentCrawlerPy, LogMessageCons, LogSourceCons
from app.common.enums import TaskProductPageType
from app.model.comment import Comment
from app.service.abnormal_processing_service import wait_load, safe_continue, persist_find_elements, safe_find_element, \
    persist_find_element
from app.service.chrome_driver_service import get_url, scroll_bottom, scroll_top, get_text, move_to_element
from app.service.database_service import insert_data
from app.service.identifiers.task_product_identifier import get_type, get_product_id
from app.service.log import log


def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver, False)
    safe_continue(driver)
    match get_type(driver):
        case TaskProductPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    crawDate = page_type = product_id = comment = date = pattern = CommentCrawlerPy.BLANK_DATA
    success = True

    craw_date = datetime.now(TIME_ZONE)
    page_type = TaskProductPageType.TM.value
    product_id = get_product_id(get_url(driver), TaskProductPageType.TM)

    show_button_element = persist_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_SHOW_BUTTON)
    move_to_element(driver, show_button_element, click=True)
    sort_div_element = persist_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_SORT_DIV)
    time.sleep(1)
    move_to_element(driver, sort_div_element, click=True)
    time.sleep(1)
    sort_by_date_element = persist_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_SORT_BYDATE)
    move_to_element(driver, sort_by_date_element, click=True)
    persist_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_COMMENT, duration=1, retry=120)
    past_size = 0
    in_date = True
    left_drawer_element = persist_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_COMMENTS)
    while in_date:
        start_time = time.time()
        if past_size == (new_size := (len(comment_elements := persist_find_elements(driver, By.XPATH, CommentCrawlerPy.XPATH_COMMENT)))):
            for _ in range(4):
                time.sleep(1)
                while safe_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_LOADING, log_print=False):
                    log(LogMessageCons.COMCRW_COMMENT_WAIT, LogSourceCons.COMMENT_CRAWLER, LOG_PRINT)
                if past_size != (new_size := (len(comment_elements := persist_find_elements(driver, By.XPATH, CommentCrawlerPy.XPATH_COMMENT)))): break
                scroll_top(driver, left_drawer_element)
                scroll_bottom(driver, left_drawer_element)
        if past_size == new_size:
            log(LogMessageCons.COMCRW_COMMENT_END, LogSourceCons.COMMENT_CRAWLER, LOG_PRINT)
            break
        for i in range(past_size, new_size):
            comment_element = comment_elements[i]
            parts_element = safe_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_META, source_element=comment_element)
            parts = get_text(driver, parts_element).split(CommentCrawlerPy.COMMENT_SPLIT)
            date_string = parts[0].strip()
            date = datetime.strptime(date_string, CommentCrawlerPy.DATE_FORMAT).date()
            if date < craw_date.date()  - timedelta(days=IN_DATE):
                in_date = False
                break
            pattern = parts[1].strip()
            comment_element = safe_find_element(driver, By.XPATH, CommentCrawlerPy.XPATH_COMMENT_STR, source_element=comment_element)
            comment = get_text(driver, comment_element)
            success = success and insert_data(conn, Comment(craw_date, page_type, product_id, comment, date, pattern))
        stay_time = time.time() - start_time
        if stay_time < 10:
            time.sleep(10 - stay_time)
        if in_date: scroll_bottom(driver, left_drawer_element)
        past_size = new_size
    return success











