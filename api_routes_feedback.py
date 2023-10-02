from app import app, request, db, logging
from customer_response import CustomerResponse
from product import ProductResponse
from utils import strToBool
import datetime as dt
from models import Customer, Product, Feedback, ProductFeedback

@app.route('/add/brand/feedback', methods=['POST'])
def add_product_feedback():
    data = request.get_json()
    if all(key in data for key in ('heading',
                                   'body',
                                   'customerid',
                                   'nps')):
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
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400

@app.route('/add/product/feedback', methods=['POST'])
def add_brand_feedback():
    data = request.get_json()
    if all(key in data for key in ('customerid',
                                   'productid',
                                   'heading',
                                   'body',
                                   'nps')):
        productFeedback = ProductFeedback(customer_id=data['customerid'],
                                          product_id=data['productid'],
                                          heading=data['heading'],
                                          body=data['body'],
                                          nps=int(data['nps']),
                                          date=dt.datetime.now())
        with app.app_context():
            db.session.add(productFeedback)
            db.session.commit()
        logging.info("Product feedback added")
        return 'Product feedback added', 200
    else:
        logging.error("Wrong query parameters")
        return "Wrong query parameters", 400
