from urllib.parse import urlparse

from app.common.enums import TaskSellerPageType
from app.service.chrome_driver_service import get_url

def get_type(driver):
    if (url := get_url(driver)) is not None and ".tmall.com" in url: return TaskSellerPageType.TM
    return None

def get_seller_id(url, page_type):
    match page_type:
        case TaskSellerPageType.TM:
            try:
                netloc = urlparse(url).netloc
                if netloc.endswith(".tmall.com"):
                    seller_id = netloc.split(".")[0]
                    return seller_id
            except Exception:
                pass
            return None
    return None