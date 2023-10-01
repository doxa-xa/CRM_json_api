from app import app, request, db, logging
from product import ProductResponse
from utils import strToBool
import datetime as dt
from models import Product

@app.route('/api/get/product')
def api_get_product():
    data = request.get_json()
    if 'id' in data.keys():
        id = data['id']
        product = Product.query.filter_by(id=id).first()
        if product:
            logging.info("Get product")
            return ProductResponse(product=product).json_response(), 200
        else:
            logging.warning(f'No product under productid {id}')
            return f'No product under productid {id}', 404
    elif 'name' in data.keys():
        name = data['name']
        products = Product.query.filter_by(name=name).all()
        result = []
        if products:
            for product in products:
                result.append(ProductResponse(product).json_response())
            logging.info("Get products")
            return result, 200
        else:
            logging.warning(f'No products under: {name}')
            return f'No products under: {name}', 404
    elif 'customerid' in data.keys():
        customerid = data['customerid']
        products = Product.query.filter_by(customer_id=customerid).all()
        result = []
        if products:
            for product in products:
                result.append(ProductResponse(product).json_response())
            logging.info("Customer products")
            return result, 200
        else:
            logging.info("Customer has no products assinged")
            return "Customer has no products assinged", 200
    else:
        logging.error('Wrong query parameters')
        return 'Wrong query parameters', 400
    

@app.route('/api/add/product',methods=['POST'])
def add_product_api():
    data = request.get_json()
    id = data['customerid']
    name = data['name']
    price = data['price']
    purchased = data['purchased']
    wrnty = data['warranty']
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
    logging.info(f'Product: {name} added to customer id: {id}')
    return f'Product: {name} added to customer id: {id}', 200

@app.route('/api/delete/product', methods=['POST'])
def api_delete_product():
    data = request.get_json()
    if 'id' in data.keys():
        id = data['id']
        product = Product.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            logging.info('Product has been deleted')
            return 'Product has been deleted', 200
        else:
            logging.warning('Product id not found')
            return 'Product id not found', 404
    elif 'customerid' in data.keys():
        customerid = data['customerid']
        products = Product.query.filter_by(customer_id=customerid).all()
        if products:
            for product in products:
                db.session.delete(product)
            db.session.commit()
            logging.info('Product(s) has been deleted')
            return 'Product(s) has been deleted', 200
        else:
            logging.warning("No products found under this customer id")
            "No products found under this customer id", 404
    else:
        logging.error("Wrong query parameters")
        return "Wrong query parameters", 400

@app.route('/api/update/product', methods=['POST'])
def api_update_product():
    data = request.get_json()
    if 'id' in data.keys():
        product = Product.query.filter_by(id=data['id']).first()
        if 'warranty' in data.keys():
            if int(data['warranty']) >1:
                product.warranty = dt.datetime.now().replace(year=product.warranty.year+int(data['warranty']))
            else:
                product.warranty = dt.datetime.now()
            db.session.commit()
            logging.info("Product warranty has been updated")
            return "Product warranty has been updated", 200   
        elif 'changeto' in data.keys():
            product.customer_id = data['changeto']
            db.session.commit()
            logging.info("Product ownership has been updated")
            return "Product ownership has been updated", 200
        else:
            logging.warning("changeto argument missing")
            return "changeto argument missing", 400
    else:
        logging.error("Wrong query parameters")
        return "Wrong query parameters", 400
        