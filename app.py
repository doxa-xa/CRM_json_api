from flask import Flask, request, url_for, jsonify, render_template, Response, send_from_directory
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from models import Customer, Product, db
from customer_response import CustomerResponse
from product import ProductResponse
from utils import strToBool
import logging
import datetime as dt

UPLOAD_FOLDER = './uploaded'
ALLOWED_EXTENTIONS = {'xls','xlsx'}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()

# GET routes -------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('addproduct.html')

#Query customer by id
@app.route('/customerid=<int:id>')
def get_customer(id):
    cust = db.get_or_404(Customer,id)
    if cust:
        customer = CustomerResponse(cust)
        app.logger.info("%s cutomer found")
        return customer.json_response(), 200
    else:
        app.logger.warning("%s customer not found")
        return "Customer Not Found", 404
    
#Query product by id
@app.route('/productid=<int:id>')
def get_product(id):
    item = db.get_or_404(Product,id)
    if item:
        product = ProductResponse(item)
        app.logger.info("%s customer found")
        return product.json_response(), 200
    else:
        app.loger.info("%s customer not found")
        return "Customer Not Found", 404

#POST routes ------------------------------------------------

#Adding product
@app.route('/add/product',methods=['POST'])
def add_product():
    id = request.form.get('customerid')
    name = request.form.get('name')
    price = request.form.get('price')
    purchased = request.form.get('purchased')
    print(purchased)
    wrnty = request.form.get('warranty')
    date = purchased.split('-')
    yyyy = int(date[0])+int(wrnty)
    mm = int(date[1])
    dd = int(date[2])
    warranty = dt.date(yyyy,mm,dd)
    product = Product(
        name = name,
        price = float(price),
        purchased = dt.datetime.strptime(purchased, "%Y-%m-%d"),
        customer_id = int(id),
        warranty = warranty
    )
    with app.app_context():
        db.session.add(product)
        db.session.commit()
    app.logging.info(f"Product: {name} added to customer id: {id}")
    return f'Product: {name} added to customer id: {id}', 200

#adding customer
@app.route('/add/customer',methods=['POST'])
def add_customer():
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    status = request.form.get('status')
    updated = dt.datetime.now()
    #contracted = request.form.get('contracted')
    opt_phone = request.form.get('optphone')
    opt_email = request.form.get('optemail')
    opt_chat = request.form.get('optchat')
    customer = Customer(name=name,
                        address=address,
                        phone=phone,
                        email=email,
                        status=status,
                        opt_chat=strToBool(opt_chat),
                        opt_phone=strToBool(opt_phone),
                        opt_email=strToBool(opt_email),
                        last_updated=updated,
                       )
    with app.app_context():
        db.session.add(customer)
        db.session.commit()
    app.logging.info(f"Customer: {name} added")
    return "customer added", 200

logging.basicConfig(filename='./api.log',level=logging.INFO)
import api_routes_customer
import api_routes_product 
import api_routes_feedback
import api_routes_customer_requests

if __name__ == '__main__':
    app.run(debug=True)

