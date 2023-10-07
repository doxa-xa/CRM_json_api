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
    
class FeedbackResponse:
    def __init__(self,feedback):
        self.id = feedback.id
        self.heading = feedback.heading
        self.body = feedback.body
        self.customer_id = feedback.customer_id
        self.date = feedback.date
        self.nps = feedback.nps
    
    def get_json(self):
        return {
            'id':self.id,
            'heading':self.heading,
            'body':self.body,
            'date':self.date,
            'nps':self.nps,
            'customerid':self.customer_id
        }

class ProductFeedbackResponse:
    def __init__(self,feedback):
        self.id = feedback.id
        self.heading = feedback.heading
        self.body = feedback.body
        self.customer_id = feedback.customer_id
        self.product_id = feedback.product_id
        self.date = feedback.date
        self.nps = feedback.nps

    def get_json(self):
        return {
            'id':self.id,
            'heading':self.heading,
            'body':self.body,
            'date':self.date,
            'nps':self.nps,
            'customerid':self.customer_id,
            'productid':self.product_id
        }