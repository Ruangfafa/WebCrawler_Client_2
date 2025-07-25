import re

from app.common.constants import TaskTagIdentifierPy
from app.common.enums import TaskTagPageType
from app.service.chrome_driver_service import get_url


def get_type(driver):
    if (url := get_url(driver)) is not None and TaskTagIdentifierPy.URL_TMALL in url: return TaskTagPageType.TM
    return None

def get_seller_id(url, page_type):
    match page_type:
        case TaskTagPageType.TM:
            try:
                match = re.search(TaskTagIdentifierPy.SELLER_ID, url, re.IGNORECASE)
                if match:
                    return match.group(1)
            except Exception:
                pass
    return None

def get_c_id(url, page_type):
    match page_type:
        case TaskTagPageType.TM:
            match_cp_c = re.search(TaskTagIdentifierPy.REGEX_CATEGORY_C, url)
            if match_cp_c:
                return match_cp_c.group(1)
            return None

def get_p_id(url, page_type):
    match page_type:
        case TaskTagPageType.TM:
            match_cp_p = re.search(TaskTagIdentifierPy.REGEX_CATEGORY_P, url)
            if match_cp_p:
                return match_cp_p.group(1)
            return None