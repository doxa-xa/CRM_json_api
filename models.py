from flask_sqlalchemy import SQLAlchemy
import datetime as dt

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    opt_email = db.Column(db.Boolean, nullable=False, default=False)
    opt_phone = db.Column(db.Boolean, nullable=False, default=False)
    opt_chat = db.Column(db.Boolean, nullable=False, default=False) 
    status = db.Column(db.String, nullable=False, default='active')
    products = db.relationship('Product',backref='customer', lazy=True)
    revenue = db.Column(db.Float, nullable=False, default=0.0)
    last_updated = db.Column(db.DateTime, nullable=False, default=dt.datetime.now().strftime("%d.%m.%Y-%H:%M"))
    last_contacted = db.Column(db.DateTime)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    purchased = db.Column(db.DateTime, nullable=False, default=dt.datetime.now())
    #deafault item warranty is 2 years
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    warranty = db.Column(db.DateTime, nullable=False)
    review = db.relationship('ProductFeedback', backref='product', lazy=True)

#TODO - Feedback from customer

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=dt.datetime.now())
    nps = db.Column(db.Integer, nullable=False, default=0)

class ProductFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=dt.datetime.now())
    nps = db.Column(db.Integer, nullable=False, default=0)

class CustomerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=dt.datetime.now())
    resolved = db.Column(db.Boolean, default=False)
    resolution = db.Column(db.String)
    resolution_date = db.Column(db.DateTime)