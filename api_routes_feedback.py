from app import app, request, db, logging
from customer_response import CustomerResponse
from product import ProductResponse, FeedbackResponse, ProductFeedbackResponse
from utils import strToBool
import datetime as dt
from models import Customer, Product, Feedback, ProductFeedback

@app.route('/api/add/brand/feedback', methods=['POST'])
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

@app.route('/api/add/product/feedback', methods=['POST'])
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
    
@app.route('/api/get/brand/feedback')
def api_get_brand_feedback():
    data = request.get_json()
    if 'customerid' in data.keys():
        feedbacks = Feedback.query.filter_by(id=data['customerid']).all()
        if feedbacks:
            result = []
            for feedback in feedbacks:
                result.append(FeedbackResponse(feedback).get_json())
            logging.info('Brand feedback records retrieved')
            return result, 200
        else:
            logging.warning('No feedback found for this customer')
            return 'No feedback found for this customer', 404
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400
    
@app.route('/api/get/product/feedback')
def api_get_product_feedback():
    data = request.get_json()
    if 'customerid' in data.keys():
        feedbacks = ProductFeedback.query.filter_by(customer_id=data['customerid']).all()
        if feedbacks:
            result = []
            for feedback in feedbacks:
                result.append(ProductFeedbackResponse(feedback).get_json())
            logging.info('Brand feedback records retrieved')
            return result, 200
        else:
            logging.warning('No feedback found for this customer')
            return 'No feedback found for this customer', 404
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400

