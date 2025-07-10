class Seller:
    def __init__(self, craw_date, page_type, seller_id, name, location, subscribe, quality_score, security_score, logistics_score):
        self.craw_date = craw_date
        self.page_type = page_type
        self.seller_id = seller_id
        self.name = name
        self.location = location
        self.subscribe = subscribe
        self.quality_score = quality_score
        self.security_score = security_score
        self.logistics_score = logistics_score