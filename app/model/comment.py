class Comment:
    def __init__(self, craw_date, page_type, product_id, comment, date, pattern):
        self.craw_date = craw_date
        self.page_type = page_type
        self.product_id = product_id
        self.comment = comment
        self.date = date
        self.pattern = pattern