class ProductResponse:
    def __init__(self, product):
        self.id = product.id
        self.name = product.name
        self.purchased = product.purchased
        self.warranty = product.warranty
        self.price = product.price

    def json_response(self):
        return {
            "id":self.id,
            "name":self.name,
            "purchase_date":self.purchased,
            "warranty":self.warranty,
            "price":self.price
        }