import datetime as dt

class CustomerResponse:
    def __init__(self,customer):
        self.id = customer.id
        self.name = customer.name
        self.address = customer.address
        self.email = customer.email
        self.phone = customer.phone
        self.optEmail = customer.opt_email
        self.optPhone = customer.opt_phone
        self.optChat = customer.opt_chat
        self.status = customer.status
        #self.products = customer.products
        self.revenue = customer.revenue
        self.lastUpdated = customer.last_updated
        self.lastContacted = customer.last_contacted

    def json_response(self):
        return {
            "id":self.id,
            "name":self.name,
            "address":self.address,
            "phone":self.phone,
            "email":self.email,
            "status":self.status,
            "revenue":self.revenue,
            "optPhone":self.optPhone,
            "optEmail":self.optEmail,
            "optChat":self.optChat,
            "lastUpdated":self.lastUpdated,
            "lastContacted":self.lastContacted
        }
    
class CustomerRequestResponse:
    def __init__(self,customerRequest):
        self.id = customerRequest.id
        self.request = customerRequest.request
        self.customer_id = customerRequest.customer_id
        self.request_date = customerRequest.request_date
        self.resolved = customerRequest.resolved
        self.resolution = customerRequest.resolution
        self.resolution_date = customerRequest.resolution_date

    def get_json(self):
        return {
            'id':self.id,
            'request':self.request,
            'customer_id':self.customer_id,
            'requestDate':self.request_date,
            'resolved':self.resolved,
            'resolution':self.resolution,
            'resolutionDate':self.resolution_date
        }