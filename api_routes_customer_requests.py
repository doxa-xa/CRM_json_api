from app import app, request, db, logging
from customer_response import CustomerResponse, CustomerRequestResponse
from product import ProductResponse
from utils import strToBool
import datetime as dt
from models import Customer, Product, CustomerRequest

@app.route('/api/open/customer/request',methods=['POST'])
def api_open_customer_request():
    data = request.get_json()
    if all(key in data for key in ('request','customerid')):
        customerRequest = CustomerRequest(request=data['request'],
                                          customer_id=data['customerid'])
        db.session.add(customerRequest)
        db.session.commit()
        logging.info('Customer request has been registered')
        return 'Customer request has been registered', 200
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400
    
@app.route('/api/close/customer/request', methods=['POST'])
def api_close_customer_request():
    data = request.get_json()
    if all( key in data for key in ('id','resolved','resolution')):
        customerRequest = CustomerRequest.query.filter_by(id=data['id']).first()
        if customerRequest:
            customerRequest.resolved = strToBool(data['resolved'])
            customerRequest.resolution = data['resolution']
            customerRequest.resolution_date = dt.datetime.now()
            db.session.commit()
            logging.info('resolution ticket has been updated')
            return 'Resolution ticket has been updated', 200
        else:
            logging.warning('No Customer request found on record')
            return 'No customer request found' , 404
    else:
        logging.error('Wrong query parameters')
        return 'wrong query parameters' ,400
    
@app.route('/api/get/customer/request')
def api_get_customer_request():
    data = request.get_json()
    if 'id' in data.keys():
        customerRequest = CustomerRequest.query.filter_by(id=data['id']).first()
        if customerRequest:
            crr = CustomerRequestResponse(customerRequest)
            logging.info('CustomerRequest fetched')
            return crr.get_json(), 200
        else:
            logging.warning("No Cusomer found")
            return 'No customer request found', 404
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400