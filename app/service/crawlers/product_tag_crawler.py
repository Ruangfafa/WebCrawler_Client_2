from datetime import datetime

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE
from app.common.constants import ProductTagCrawlerPy
from app.common.enums import TaskTagPageType
from app.model.product_tag import ProductTag
from app.service.abnormal_processing_service import wait_load, safe_continue, persist_find_elements, safe_get_attribute, \
    safe_find_elements, safe_find_element, persist_find_element
from app.service.chrome_driver_service import get_url, get_text
from app.service.database_service import insert_data
from app.service.identifiers.task_tag_identifier import get_type, get_seller_id, get_cp_id


def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver, False)
    safe_continue(driver)
    match get_type(driver):
        case TaskTagPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    craw_date = page_type = cp_id = seller_id = product_id = sold = ProductTagCrawlerPy.BLANK_DATA
    success = more_page = True

    craw_date = datetime.now(TIME_ZONE)
    page_type = TaskTagPageType.TM.value
    cp_id = get_cp_id(get_url(driver), TaskTagPageType.TM)
    seller_id = get_seller_id(get_url(driver), TaskTagPageType.TM)

    while more_page:
        all_multi_product_divs = persist_find_elements(driver, By.XPATH, ProductTagCrawlerPy.XPATH_ALL_PRODUCT_DIVS)
        tag_multi_product_divs = []
        for multi_product_div in all_multi_product_divs:
            if safe_get_attribute(driver, multi_product_div, ProductTagCrawlerPy.ATTRIBUTE_CLASS) == ProductTagCrawlerPy.CLASS_PAGINATION: break
            tag_multi_product_divs.append(multi_product_div)
        for multi_product_div in tag_multi_product_divs:
            product_divs = safe_find_elements(driver, By.XPATH, ProductTagCrawlerPy.XPATH_PRODUCT, source_element=multi_product_div)
            for product_div in product_divs:
                product_id = safe_get_attribute(driver, product_div, ProductTagCrawlerPy.ATTRIBUTE_DATA_ID)
                sold_element = safe_find_element(driver, By.XPATH, ProductTagCrawlerPy.XPATH_SOLD, source_element=product_div)
                sold = get_text(driver, sold_element)
                success = success and insert_data(conn, ProductTag(craw_date, page_type, cp_id, seller_id, product_id, sold))
        page_info_element = persist_find_element(driver, By.XPATH, ProductTagCrawlerPy.XPATH_PAGE_INFO)
        page_info = get_text(driver, page_info_element)
        if is_last_page(page_info): break
        page_next_element = persist_find_element(driver, By.XPATH, ProductTagCrawlerPy.XPATH_PAGE_NEXT)
        page_next = safe_get_attribute(driver, page_next_element, ProductTagCrawlerPy.ATTRIBUTE_HREF)
        driver.get(page_next)
        wait_load(driver, False)
        safe_continue(driver)
    return success

def is_last_page(page_info: str) -> bool:
    try:
        current, total = map(int, page_info.strip().split('/'))
        return current >= total
    except Exception:
        return False  # 出现格式错误时不认为是最后一页







