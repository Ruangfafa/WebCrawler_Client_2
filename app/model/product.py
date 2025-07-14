class Product:
    def __init__(self, craw_date, page_type, product_id, title, sold365, address, garantee, parameter, pattern_com, sku_id, pattern, orgn_price, disk_price):
        self.craw_date = craw_date
        self.page_type = page_type
        self.product_id = product_id
        self.title = title
        self.sold365 = sold365
        self.address = address
        self.garantee = garantee
        self.parameter = parameter
        self.pattern_com = pattern_com
        self.sku_id = sku_id
        self.pattern = pattern
        self.orgn_price = orgn_price
        self.disk_price = disk_price
