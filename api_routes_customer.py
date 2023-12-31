from app import app, request, db, logging, send_from_directory
from customer_response import CustomerResponse
from product import ProductResponse
from utils import strToBool, check_keys, export_customers
import datetime as dt, openpyxl
from models import Customer, Product

@app.route('/api/get/customer')
def api_get_customer():
    turnover = 0.0
    data = request.get_json()
    if 'id' in data.keys():
        id = int(data['id'])
        customer = Customer.query.filter_by(id=id).first()
        if customer:
            products = Product.query.filter_by(customer_id=id).all()
            if products:
                for product in products:
                    turnover += product.price
                if turnover != customer.revenue:
                    customer.revenue = turnover
                    db.session.commit
            response = CustomerResponse(customer)
            logging.info(f'Get customer request successful')
            return response.json_response(), 200
        else:
            logging.warning(f"Customer id:{id} is not found", 404)
            return f"CustomerID: {id} not found", 404
    elif 'name' in data.keys():
        name = data['name']
        customers = Customer.query.filter_by(name=name).all()
        if customers:
            result = []
            for customer in customers:
                result.append(CustomerResponse(customer).json_response())
            logging.info(f'Get customer request successful')
            return result, 200
        else:
            logging.warning(f"{name} is not found")
            return f"{name} is not found", 404
    else:
        logging.error("Wrong query parameters. No such id or name")
        return "Wrong query parameters. No such id or name", 400


@app.route('/api/add/customer',methods=['POST'])
def add_customer_api():
    data = request.get_json()
    name = data["name"]
    address = data['address']
    if 'phone' in data.keys():
        phone = data['phone']
    else:
        phone = None
    email = data['email']
    status = data['status']
    updated = dt.datetime.now() #.strftime("%d.%m.%Y-%H:%M")
    #contracted = request.form.get('contracted')
    opt_phone = strToBool(data['optphone'])
    opt_email = strToBool(data['optemail'])
    opt_chat = strToBool(data['optchat'])
    customer = Customer(name=name,
                        address=address,
                        phone=phone,
                        email=email,
                        status=status,
                        opt_chat=opt_chat,
                        opt_phone=opt_phone,
                        opt_email=opt_email,
                        last_updated=updated,
                       )
    with app.app_context():
        db.session.add(customer)
        db.session.commit()
    logging.info("customer added")
    return "customer added", 200

@app.route('/api/delete/customer')
def api_delete_customer():
    data = request.get_json()
    if 'id' in data.keys():
        id = data['id']
        customer = Customer.query.filter_by(id=id).first()
        products = Product.query.filter_by(customer_id=id).all()
        if customer:
            if products:
                result = []
                for product in products:
                    result.append(ProductResponse(product).json_response())
                return f"Customer {customer.name} has {len(result)} products assigned. Operation cannot be completed", 403
            else:
                message = f'CustomerID: {customer.id} - {customer.name} has been deleted'
                db.session.delete(customer)
                db.session.commit()
                logging.info(message)
                return message, 200
        else:
            logging.warning("No such customer on record")
            return "No such customer on record", 404

@app.route('/api/update/customer',methods=['POST'])
def api_update_customer():
    data = request.get_json()
    if 'id' in data.keys():
        id = data['id']
        customer = Customer.query.filter_by(id=id).first()
        if customer:
            if 'email' in data.keys():
                customer.email = data['email']
            elif 'phone' in data.keys():
                customer.phone = data['phone']           
            elif 'address' in data.keys():
                customer.address = data['address']
            elif 'status' in data.keys():
                customer.status = data['status']
            elif 'optemail' in data.keys():
                customer.opt_email = strToBool(data['optemail'])
            elif 'optphone' in data.keys():
                customer.opt_phone = strToBool(data['optphone'])
            elif 'optchat' in data.keys():
                customer.opt_chat = strToBool(data['optchat'])
            else:
                logging.error("Wrong query parameters")
                return "Wrong query parameters", 400
            customer.last_updated = dt.datetime.now()
            db.session.commit()
            logging.info('Customer updated successfuly')
            return 'Customer updated successfuly', 200
        else:
            logging.warning("No such customer on record")
            return "No such customer on record", 404
        
@app.route('/api/customer/export')
def api_customer_export():
    data = request.get_json()
    if check_keys(('name','surname','email'),data.keys()):
        logging.info(f"{data['name']} {data['surname']} with {data['email']} initiated export of customer data")
        excel_file = export_customers()
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'] ,path=excel_file, as_attachment=True)
        logging.warning('No customer records')
        return 'No customer records', 404
    logging.error('Wrong query parameters')
    return 'Wrong query parameters', 400


