import re

from app.common.constants import TaskSellerIdentifierPy
from app.common.enums import TaskSellerPageType
from app.service.chrome_driver_service import get_url

def get_type(driver):
    if (url := get_url(driver)) is not None and TaskSellerIdentifierPy.URL_TMALL in url: return TaskSellerPageType.TM
    return None

def get_seller_id(url, page_type):
    match page_type:
        case TaskSellerPageType.TM:
            try:
                match = re.search(TaskSellerIdentifierPy.SELLER_ID, url, re.IGNORECASE)
                if match:
                    return match.group(1)
            except Exception:
                pass
    return None