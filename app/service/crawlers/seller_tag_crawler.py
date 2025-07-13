import re
from datetime import datetime

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE
from app.common.constants import SellerTagCrawlerPy
from app.common.enums import TaskSellerPageType
from app.model.seller_tag import SellerTag
from app.service.abnormal_processing_service import wait_load, persist_find_elements, persist_find_element, persist_get_attribute, safe_continue, safe_find_elements
from app.service.chrome_driver_service import get_url, get_text
from app.service.database_service import insert_data
from app.service.identifiers.task_seller_identifier import get_type, get_seller_id

def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver, False)
    safe_continue(driver)
    match get_type(driver):
        case TaskSellerPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    craw_date = page_type = seller_id = tag = cp_id = SellerTagCrawlerPy.BLANK_DATA
    success = True

    craw_date = datetime.now(TIME_ZONE)
    page_type = TaskSellerPageType.TM.value
    seller_id = get_seller_id(get_url(driver), TaskSellerPageType.TM)

    insert_data(conn, SellerTag(craw_date, page_type, seller_id, SellerTagCrawlerPy.ALL_PRODUCT, SellerTagCrawlerPy.CATEGORY_ALL_PREFIX))
    c_tags = persist_find_elements(driver, By.XPATH, SellerTagCrawlerPy.XPATH_C_PROPS)
    for c_tag in c_tags:
        c_tag_element = persist_find_element(driver, By.XPATH, SellerTagCrawlerPy.XPATH_C_TAG, source_element=c_tag)
        tag = get_text(driver, c_tag_element)
        href = persist_get_attribute(driver, c_tag_element, SellerTagCrawlerPy.ATTRIBUTE_HREF)
        match = re.search(SellerTagCrawlerPy.REGEX_CATEGORY_C, href)
        if match:
            cp_id = SellerTagCrawlerPy.CATEGORY_C_PREFIX % match.group(1)
        success = success and insert_data(conn, SellerTag(craw_date, page_type, seller_id, tag, cp_id))
        if cc_tags := safe_find_elements(driver, By.XPATH, SellerTagCrawlerPy.XPATH_CC_PROPS, source_element=c_tag):
            for cc_tag in cc_tags:
                cc_tag_element = persist_find_element(driver, By.XPATH, SellerTagCrawlerPy.XPATH_CC_TAG, source_element=cc_tag)
                tag_child = get_text(driver, cc_tag_element)
                href = persist_get_attribute(driver, cc_tag_element, SellerTagCrawlerPy.ATTRIBUTE_HREF)
                match = re.search(SellerTagCrawlerPy.REGEX_CATEGORY_C, href)
                if match:
                    cp_id = SellerTagCrawlerPy.CATEGORY_C_PREFIX % match.group(1)
                success = success and insert_data(conn, SellerTag(craw_date, page_type, seller_id, SellerTagCrawlerPy.CATEGORY_CC_PREFIX_TAG % (tag, tag_child), cp_id))

    props = persist_find_elements(driver, By.XPATH, SellerTagCrawlerPy.XPATH_P_PROPS)
    for prop in props:
        prop_element = persist_find_element(driver, By.XPATH, SellerTagCrawlerPy.XPATH_P_PROP_KEY, source_element=prop)
        prop_name = get_text(driver, prop_element)
        p_tags = persist_find_elements(driver, By.XPATH, SellerTagCrawlerPy.XPATH_P_TAGS, source_element=prop)
        for p_tag in p_tags:
            href = persist_get_attribute(driver, p_tag, SellerTagCrawlerPy.ATTRIBUTE_HREF)
            match = re.search(SellerTagCrawlerPy.REGEX_CATEGORY_P, href)
            if match:
                cp_id = SellerTagCrawlerPy.CATEGORY_P_PREFIX % match.group(1)
            tag = SellerTagCrawlerPy.CATEGORY_P_PREFIX_TAG % (prop_name, get_text(driver, p_tag))
            success = success and insert_data(conn, SellerTag(craw_date, page_type, seller_id, tag, cp_id))
    return success