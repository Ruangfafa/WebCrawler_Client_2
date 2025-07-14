import re

from app.common.constants import TaskProductIdentifierPy
from app.common.enums import TaskProductPageType
from app.service.chrome_driver_service import get_url


def get_type(driver):
    if (url := get_url(driver)) is not None and TaskProductIdentifierPy.URL_TMALL in url: return TaskProductPageType.TM
    return None

def get_product_id(url, page_type):
    match page_type:
        case TaskProductPageType.TM:
            try:
                match = re.search(TaskProductIdentifierPy.PRODUCT_ID, url, re.IGNORECASE)
                if match:
                    return match.group(1)
            except Exception:
                pass
    return None