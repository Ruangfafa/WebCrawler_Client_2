from datetime import datetime

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE, LOG_PRINT
from app.common.constants import SellerCrawlerPy
from app.model.seller import Seller
from app.service.abnormal_processing_service import wait_load, persist_find_element, persist_find_elements
from app.service.chrome_driver_service import get_url, move_to_element, move_by_offset
from app.service.database_service import insert_data
from app.service.identifiers.task_seller_identifier import get_type, get_seller_id
from app.common.enums import TaskSellerPageType
from app.service.log import log


def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver)
    match get_type(driver):
        case TaskSellerPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    craw_date = page_type = seller_id = name = location = subscribe = quality_score = security_score = logistics_score = None

    craw_date = datetime.now(TIME_ZONE)  # 包含完整日期时间
    page_type = TaskSellerPageType.TM.value
    seller_id = get_seller_id(get_url(driver), TaskSellerPageType.TM)
    name_elem = persist_find_element(driver, By.XPATH, SellerCrawlerPy.XPATH_NAME)
    if name_elem: name = name_elem.text.strip()
    # 鼠标先尝试移动到三角按钮触发弹窗
    triangle_icon = persist_find_element(driver, By.XPATH, SellerCrawlerPy.XPATH_LOCATION_TRIANGLE)
    if not move_to_element(driver, triangle_icon): pass
    # 尝试点击修复异常行为（鼠标偏移）
    move_by_offset(driver, 1000, 1000, True)
    if not move_to_element(driver, triangle_icon, True): pass
    # 使用重复查找机制获取地址字段
    location_elem = persist_find_element(driver, By.XPATH, SellerCrawlerPy.XPATH_LOCATION, 0.5, 18)
    if location_elem: location = location_elem.text.strip()
    score_elements = persist_find_elements(driver, By.XPATH, SellerCrawlerPy.XPATH_SCORE_ELEMENTS)
    if len(score_elements) == 3:
        quality_score = score_elements[0].text.strip()
        security_score = score_elements[1].text.strip()
        logistics_score = score_elements[2].text.strip()

    return insert_data(conn, Seller(craw_date, page_type, seller_id, name, location, subscribe, quality_score, security_score, logistics_score))



