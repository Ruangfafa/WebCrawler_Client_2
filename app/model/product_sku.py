class ProductSku:
    def __init__(self, craw_date, page_type, product_id, sku_id, pattern, orgn_price, disc_price):
        self.craw_date = craw_date
        self.page_type = page_type
        self.product_id = product_id
        self.sku_id = sku_id
        self.pattern = pattern
        self.orgn_price = orgn_price
        self.disc_price = disc_price