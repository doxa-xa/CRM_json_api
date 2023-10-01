from app import app, request, db, logging
from customer_response import CustomerResponse
from product import ProductResponse
from utils import strToBool
import datetime as dt
from models import Customer, Product, Feedback

@app.route('/add/product/feedback', methods=['POST'])
def add_product_feedback():
    data = request.get_json()
    if 'heading' and 'customerid' in data.keys():
        if 'body' and 'nps' in data.keys():
            feedback = Feedback(
                heading = data['heading'],
                body = data['body'],
                customer_id = int(data['customerid']),
                nps = int(data['nps']),
                date = dt.datetime.now()
            )
            with app.app_context():
                db.session.add(feedback)
                db.session.commit()
            logging.info('Feedback saved')
            return 'Feedback saved', 200
        else:
            logging.warning('Feedback request is missing body or nps score. Please refer to the documentation')
            return 'Feedback request is missing body or nps score. Please refer to the documentation', 400
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400

@app.route('/add/brand/feedback', methods=['POST'])
def add_brand_feedback():
    pass