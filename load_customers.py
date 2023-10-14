from app import app, request, db, logging, ALLOWED_EXTENTIONS, redirect, url_for
from customer_response import CustomerResponse, CustomerRequestResponse
from product import ProductResponse
from utils import strToBool
import datetime as dt, openpyxl, os
from models import Customer, Product, CustomerRequest
from werkzeug.utils import secure_filename

def allowed_file(file):
    return '.' in file and \
        file.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/api/customers/upload',['POST'])
def upload_customers():
    if 'filepath' in request.files:
        file = request.files['filepath']
        if file.filename == '':
            logging.warning('No file uploaded')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER']),filename)
            wb = openpyxl.load_workbook(os.path.join(app.config['UPLOAD_FOLDER']),filename)
            ws = wb.active
            if ws:
                for row in ws.iter_rows():
                    if len(row) != 5:
                        logging.warning(f'Inconsistent data in:{row}')
                        continue
                    else:
                        customer = Customer(name=row[0],
                                            email=row[1],
                                            address=row[2],
                                            phone=row[3],
                                            status=row[4])
                        db.session.add(customer)
                        db.session.commit()
                        logging.info('Record added')
                logging.info('Customer data upload successful')
                return 'Customer data upload successful', 200
            logging.error('Wrong file type or corrupted file')
            return 'Wrong file type or corrupted file', 400
    logging.error('Wrong query parameters')
    return 'Wrong query parameters', 400
    
            