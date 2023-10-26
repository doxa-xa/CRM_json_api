from models import Product, Customer
import openpyxl
import datetime as dt


now = dt.datetime.now().strftime("%d%m%Y_%H%M")

def strToBool(value):
    if value.lower() == "false" or "":
        return False
    elif value.lower() == "true":
        return True
    
def check_keys(keys,dict):
    if all(key in dict for key in keys):
        return True
    else:
         return False

def export_customers():
    customers = Customer.query.all()
    if customers:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        row = 1
        for customer in customers:
            worksheet[f'A{row}'] = customer.id
            worksheet[f'B{row}'] = customer.name
            worksheet[f'C{row}'] = customer.email
            worksheet[f'D{row}'] = customer.address
            worksheet[f'E{row}'] = customer.phone
            worksheet[f'F{row}'] = customer.opt_email
            worksheet[f'G{row}'] = customer.opt_phone
            worksheet[f'H{row}'] = customer.opt_chat
            worksheet[f'I{row}'] = customer.status
            worksheet[f'J{row}'] = customer.revenue
            worksheet[f'K{row}'] = customer.last_updated
            worksheet[f'L{row}'] = customer.last_contacted
            row += 1
        excel_file = f'customers_data{now}.xlsx' 
        workbook.save(f'uploaded/{excel_file}')
    return excel_file

def export_products():
    products = Product.query.all()
    if products:
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        row = 1
        for product in products:
            worksheet[f'A{row}'] = product.id
            worksheet[f'B{row}'] = product.name
            worksheet[f'C{row}'] = product.price
            worksheet[f'D{row}'] = product.purchased
            worksheet[f'E{row}'] = product.customer_id
            worksheet[f'F{row}'] = product.warranty
            row += 1        
        excel_file = f'products_data{now}.xlsx' 
        workbook.save(f'uploaded/{excel_file}')
    return excel_file