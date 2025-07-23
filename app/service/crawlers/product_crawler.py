import re
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from app.common.config_loader import TIME_ZONE
from app.common.constants import ProductCrawlerPy
from app.common.enums import TaskProductPageType
from app.model.product import Product
from app.model.product_sku import ProductSku
from app.service.abnormal_processing_service import wait_load, safe_continue, persist_find_element, safe_get_attribute, \
    persist_find_elements, safe_find_element
from app.service.chrome_driver_service import get_text, move_to_element, get_url
from app.service.database_service import insert_data
from app.service.identifiers.task_product_identifier import get_type, get_product_id


def craw(conn, driver, taskUrl):
    driver.get(taskUrl)
    wait_load(driver, False)
    safe_continue(driver)
    match get_type(driver):
        case TaskProductPageType.TM:
            return craw_tm(conn, driver)
    return False

def craw_tm(conn, driver):
    craw_date = page_type = product_id = title = sold365 = address = guarantee = parameter = pattern_com = sku_id = pattern = orgn_price = disk_price = ProductCrawlerPy.BLANK_DATA
    success = True

    craw_date = datetime.now(TIME_ZONE)
    page_type = TaskProductPageType.TM.value
    product_id = get_product_id(get_url(driver), TaskProductPageType.TM)
    title_element = persist_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_TITLE)
    title = safe_get_attribute(driver, title_element, ProductCrawlerPy.ATTRIBUTE_TITLE)
    sold365_element = persist_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_SOLD365)
    sold365 = get_text(driver, sold365_element)
    if sold365:
        sold365.replace(ProductCrawlerPy.DOT, ProductCrawlerPy.BLANK)
    address_element = persist_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_ADDRESS)
    address = get_text(driver, address_element)
    if address:
        address.replace(ProductCrawlerPy.TO, ProductCrawlerPy.BLANK)

    guarantee_elements = persist_find_elements(driver, By.XPATH, ProductCrawlerPy.XPATH_GUARANTEES)
    guarantees = []
    for guarantee_element in guarantee_elements:
        guarantee_text = get_text(driver, guarantee_element)
        if guarantee_text:
            guarantees.append(guarantee_text)
    guarantee = ProductCrawlerPy.INFO_CONNECTOR.join(guarantees)

    parameter_elements = persist_find_elements(driver, By.XPATH, ProductCrawlerPy.XPATH_PARAMETERS)
    parameters = []
    for parameter_element in parameter_elements:
        parameter_text = get_text(driver, parameter_element)
        if parameter_text:
            parameters.append(parameter_text)
    parameter = ProductCrawlerPy.INFO_CONNECTOR.join(parameters)

    pattern_com_elements = persist_find_elements(driver, By.XPATH, ProductCrawlerPy.XPATH_PATTERN_COMS)
    pattern_coms = []
    for pattern_com_element in pattern_com_elements:
        pattern_com_text = get_text(driver, pattern_com_element)
        if pattern_com_text:
            pattern_coms.append(pattern_com_text)
    pattern_com = ProductCrawlerPy.INFO_CONNECTOR.join(pattern_coms)

    sku_item_elements = persist_find_elements(driver, By.XPATH, ProductCrawlerPy.XPATH_SKU_ITEMS)
    sku_item_lists = []
    for sku_item_element in sku_item_elements:
        value_item_elements = persist_find_elements(driver, By.XPATH, ProductCrawlerPy.XPATH_VALUE_ITEMS, source_element=sku_item_element)
        if value_item_elements:
            sku_item_lists.append(value_item_elements)

    if not sku_item_lists:
        sku_id = pattern = ProductCrawlerPy.ONLY_PATTERN
        price_wrap_element = persist_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_PRICE_WRAP)
        highlight_price_element = safe_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_HIGHLIGHT_PRICE, source_element=price_wrap_element)
        sub_price_element = safe_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_SUB_PRICE, source_element=price_wrap_element, log_print=False)
        if sub_price_element:
            disc_price = get_text(driver, highlight_price_element)
            orgn_price = get_text(driver, sub_price_element)
        else:
            disc_price = ProductCrawlerPy.NO_DISCOUNT
            orgn_price = get_text(driver, highlight_price_element)
        success_product = insert_data(conn, Product(craw_date, page_type, product_id, title, sold365, address, guarantee, parameter, pattern_com))
        success_product_sku = insert_data(conn, ProductSku(craw_date, page_type, product_id, sku_id, pattern, orgn_price, disc_price))
        return success and success_product and success_product_sku

    current_pattern = [0] * len(sku_item_elements)

    def is_disabled(element): return ProductCrawlerPy.IS_DISABLED in element.get_attribute(ProductCrawlerPy.ATTRIBUTE_CLASS)
    def is_selected(element): return ProductCrawlerPy.IS_SELECTED in element.get_attribute(ProductCrawlerPy.ATTRIBUTE_CLASS)

    success_product = insert_data(conn, Product(craw_date, page_type, product_id, title, sold365, address, guarantee, parameter, pattern_com))
    has_next = True

    while has_next:
        valid = True
        time.sleep(5)
        for i, group in enumerate(sku_item_lists):
            if is_disabled(group[current_pattern[i]]):
                valid = False
                break
        if valid:
            for i, group in enumerate(sku_item_lists):
                element = group[current_pattern[i]]
                if not is_selected(element):
                    move_to_element(driver, element, click=True)

        pattern_list = []
        for i, group in enumerate(sku_item_lists):
            text = group[current_pattern[i]].text.strip()
            if text:
                pattern_list.append(text)
        pattern = ProductCrawlerPy.INFO_CONNECTOR.join(pattern_list) or ProductCrawlerPy.BLANK_DATA

        price_wrap_element = persist_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_PRICE_WRAP)
        highlight_price_element = safe_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_HIGHLIGHT_PRICE, source_element=price_wrap_element)
        sub_price_element = safe_find_element(driver, By.XPATH, ProductCrawlerPy.XPATH_SUB_PRICE, source_element=price_wrap_element, log_print=False)
        if sub_price_element:
            disc_price = get_text(driver, highlight_price_element)
            orgn_price = get_text(driver, sub_price_element)
        else:
            disc_price = ProductCrawlerPy.NO_DISCOUNT
            orgn_price = get_text(driver, highlight_price_element)
        current_url = get_url(driver)
        match = re.search(ProductCrawlerPy.SKU_ID, current_url)
        if match:
            sku_id = match.group(1)
        success = success and success_product and insert_data(conn, ProductSku(craw_date, page_type, product_id, sku_id, pattern, orgn_price, disc_price))

        for i in reversed(range(len(current_pattern))):
            current_pattern[i] += 1
            if current_pattern[i] < len(sku_item_lists[i]):
                break
            else:
                current_pattern[i] = 0
                if i == 0:
                    has_next = False
    return success




