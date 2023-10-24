This is a simple CRM API. 
It sends receives JSON requests.
You will need flask in order to run. 
I recomend installing Postman (or similar software) in order to test and monitor the API logic.

Actions:
1. You can use it to add, update and delete customers from a database. 
2. You can use it to add, update and delete products from a database.
3. You can assign and unassign products to customers using customerid foreign key in the products table
4. You can collect feedback from customers for brand and product questions
5. You can submit and respond to customer requests

Database type - SQLite
Responses are in JSON format

Tables:
- Customer
- CustomerRequest
- Product
- Feedback
- ProductFeedback

Endpoints:

I.Customer:
1.Add Customer:
- URL: /api/add/customer
- method: POST
- action: creates a new record to customer table
- JSON request body: 
{
    "name": required,
    "address": required,
    "phone": not requeired,
    "email": required,
    "optphone": not required,
    "optemail": not required,
    "optchat": not required,
    "status": required
}

2.Get Customer(s):
- URL: /api/get/customer
- method: GET
- action: retreives a record(s) from the customer table
* single record by id
* list of records by name
-JSON request body:
{"id": required} or {"name": required}

3.Delete Customer:
- URL: /api/delete/customer
- method: GET
- action: deletes a record from the customer table
* single record by id
! if the customer has product(s) assigned operation will not be processed. Product(s) has to be unassigned first
-JSON request body:{"id": required}

4.Update Customer:
- URL: /api/update/customer
- method: POST
- action: update a record from the product table
* single record by id
-JSON request body:{"id": required, one or many attributes requred*}
*updatable attributes: email, phone, address, status, optphone, optemail, optchat

II.Product:

1.Add Product:
- URL: /api/add/product
- method: POST
- action: creates a new record to product table
-JSON request body:
{
    "name": required,
    "price": required,
    "purchased": requeired,
    "customerid": required,
    "warranty": required
}

2.Get Product(s):
- URL: /api/get/product
- method: GET
- action: retreives a record(s) from the product table
* single record by id
* list of records by name
* list of records by customerid (if a custmer has several products assigned)
-JSON request body:{"id": required} or {"name": required} or {"customerid":requeired}

3.Delete Product:
- URL: /api/delete/product
- method: POST
- action: deletes a record(s) from the customer table
* single record by id
* multiple records by customerid
-JSON request body:{"id": required} or {"customerid":requeired}

4.Update Product:
- URL: /api/update/product
- method: POST
- action: update a record from the product table
* single record by id
-JSON request body:{"id": required, "warranty":requeired} or {"id":required, "changeto":required*}
*changeto requires and id for reassign (transfer) product(s) to customer(s)

III. Customer Feedback - currently in development

1. Brand Feedback:
- URL: /api/add/brand/feedback
- method: POST
- action: creates a record of a customer feedback for brand question
* single record by customerid
- JSON request body:{"customerid":required, "heading":required, "body":required}

2. Product Feedback:
- URL: /api/add/product/feedback
- method: POST
- action: creates a record of a customer feedback for product question
* single record by customerid, productid
- JSON request body:{"productid": required, "customerid":required, "heading":required, "body":required}

3. Get Product Feedback:
- URL: /api/get/product/feedback
- method: GET
- action: retrieves all records of a customer feedback for product question
* single record by customerid
- JSON request body:{"customerid": required}

4. Get Brand Feedback:
- URL: /api/get/brand/feedback
- method: GET
- action: retrieves all records of a customer feedback for brand question
* single record by customerid
- JSON request body:{"customerid": required}

IV. Customer Request (Tickting)

1. Open Ticket:
- URL: /api/open/customer/request
- method: POST
- actoion: creates a reacord of a customer inquiry or problem
* single record by: request, customerid
- JSON request body: {"request":required, "customerid": required}

2. Close Ticket:
- URL: /api/close/customer/request
- method: POST
- actoion: creates a reacord of a customer inquiry or problem
* single record by: id
- JSON request body: {"id":required, "resolved": required, "resolution":required }

3. Get Ticket:
- URL: /api/get/customer/request
- method: GET
- actoion: returns a reacord of a customer inquiry or problem
* single record by: id
- JSON request body: {"id":required }


V. Reporting (BI) 

1. Customer Export
- URL: /api/customer/export
- method: GET
- acion: extacts an excel worksheet of all customer records in the database
- JSON request body: {"name":required, "surname":required, "email":required}

2. Product Export
- URL: /api/product/export
- method: GET
- acion: extacts an excel worksheet of all product records in the database
- JSON request body: {"name":required, "surname":required, "email":required}

VI. Bulk DB Uploads:

1. Upload Customers File
- URL: /upload/customers
- method: POST* (Browser Web Form file upload)
- supported file types: xls, xlsx, txt, csv
- data format: 
* XLS/XLSX: [A1:Name(+Surname),B1:Email,C1:Address,D1:Phone,E1:Opt_email,F1:Opt_phone,G1:Opt_chat,H1:Status] - Opt fields are Optional Name & Email data is mandatory, fields without them will be skipped and logged.
* TXT/CSV: without headers - Opt fields are Optional Name & Email data is mandatory, fields without them will be skipped and logged.

2. Upload Products File
- URL: /upload/products
- method: POST* (Browser Web Form file upload)
- supported file types: xls, xlsx, txt, csv
- data format: 
* XLS/XLSX: [A1:Name,B1:Price,C1:Purchased,D1:Warranty,] - Name & Price data is mandatory, fields without them will be skipped and logged.
* TXT/CSV: without headers - Name & Price data is mandatory, fields without them will be skipped and logged.