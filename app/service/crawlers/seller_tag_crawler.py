from datetime import datetime

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE
from app.common.constants import SellerTagCrawlerPy
from app.common.enums import TaskSellerPageType
from app.model.seller_tag import SellerTag
from app.service.abnormal_processing_service import wait_load, persist_find_elements
from app.service.chrome_driver_service import get_url
from app.service.crawlers.seller_crawler import craw_tm
from app.service.database_service import insert_data
from app.service.identifiers.task_seller_identifier import get_type, get_seller_id


def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver)
    match get_type(driver):
        case TaskSellerPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    craw_date = page_type = seller_id = tag = cp_id = None

    craw_date = datetime.now(TIME_ZONE)  # 包含完整日期时间
    page_type = TaskSellerPageType.TM.value
    seller_id = get_seller_id(get_url(driver), TaskSellerPageType.TM)

    c_tags = persist_find_elements(conn, By.XPATH, SellerTagCrawlerPy.XPATH_C_TAGS)
    for c_tag in c_tags:
        tag_element = c_tag.get_attribute(SellerTagCrawlerPy.XPATH_ATTRIBUTE_HERF)



    return insert_data(conn, SellerTag(craw_date, page_type, seller_id, tag, cp_id))