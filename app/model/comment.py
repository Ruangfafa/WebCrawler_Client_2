class Comment:
    def __init__(self, crawDate, page_type, product_id, comment, date, pattern):
        self.crawDate = crawDate
        self.page_type = page_type
        self.product_id = product_id
        self.comment = comment
        self.date = date
        self.pattern = pattern