from flask import Flask, request,jsonify,make_response
from peewee import *
from modules import * 
from datetime import datetime 
from weasyprint import HTML

app = Flask(__name__)
db = SqliteDatabase('invoice.db')

@app.route('/customer/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def customer(id):
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        address = data.get("address")

        if username is None or not username:
            return "please provide username"
        if email is None or not email:
            return "Must be provide email"
        
        customer= Customer.create(
            username=username,
            email=email,
            address=address
        )
        return jsonify({
            "customer":{
                "customer_id":customer.id,
                "customer name":customer.username,
                "customer email":customer.email,
                "customer address":customer.address
            }
        })
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            customer = Customer.get_by_id(id)
            customer.username = data.get("username")
            customer.email = data.get("email")
            customer.address = data.get("address")
            return jsonify({
            "customer":{
                "customer_id":customer.id,
                "customer name":customer.username,
                "customer email":customer.email,
                "customer address":customer.address
            }
            })
        except DoesNotExist:
            return jsonify({
                "message": "Customer not found"
            })
    elif request.method == "DELETE":
        try:
            customer = Customer.get_by_id()
            customer.delete_instance()
            return jsonify({
                "message":f"Customer {id} delete Successfully"
            })
        except Customer.DoesNotExist:
            return "Customer Not found"   
    else:
        customer = Customer.select()
        for data in customer:
            [{
                "customer id":data.id ,
                "customer name":data.username,
                "customer email":data.email,
                "customer address":data.address
            }]

@app.route("/invoice/<string:invoice_number>", methods=['POST','PUT','DELETE','GET'])
def invoice(invoice_number):
    if request.method == "POST":
        data = request.get_json()
        invoice_number = data.get("invoice_number")
        customer_id = data.get("customer")
        customer = Customer.get_by_id(customer_id)
        total_amount = 0
        created_at = datetime.now()
        
        if  invoice_number is None or not invoice_number :
            return "please provide invoice_number"

        invoice = Invoice.create(
            invoice_number=invoice_number,
            customer=customer,
            total_amount=total_amount,
            created_at=created_at
        )
        return jsonify({
            "Invoice": {
                "Invoice_number": invoice.invoice_number,
                "customer": invoice.customer.id,
                "total_amount": invoice.total_amount,
                "created_at": str(invoice.created_at)
            }
        })

    elif request.method == "PUT":
        try:
            data = request.get_json()
            invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_number)
            if not invoice:
                return jsonify({"message": "Invoice not Found"}), 404

            customer_id = data.get("customer")
            invoice.customer = Customer.get_by_id(customer_id)
            invoice.total_amount = 0
            invoice.created_at = datetime.now()
            invoice.save()

            return jsonify({
                "Invoice": {
                   "Invoice_number": invoice.invoice_number,
                   "customer": invoice.customer.id,
                   "total_amount": invoice.total_amount,
                   "created_at": str(invoice.created_at)
                }
            })
        except:
            return jsonify({"message": "Error updating invoice"}), 500

    elif request.method == "DELETE":
        invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_number)
        if not invoice:
            return jsonify({"message": "Invoice not Found"}), 404
        invoice.delete_instance()
        return jsonify({"message": "Invoice deleted successfully"})

    else:  # GET
        invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_number)
        if not invoice:
            return jsonify({"message": "Invoice not Found"}), 404

        return jsonify({
            "Invoice_number": invoice.invoice_number,
            "Customer": invoice.customer.id,
            "total_amount": invoice.total_amount,
            "created at": str(invoice.created_at)
        })
    
@app.route('/item/<int:id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def item(id):
    if request.method == 'POST':
        data = request.get_json()
        item_name = data.get("item_name")
        invoice_id = data.get("invoice")
        invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_id)
        unit_price = data.get("unit_price")
        quantity = data.get("quantity")
        amount = float(unit_price) * int(quantity)
        
        if not item_name :
            return "please enter item_name"
        if not unit_price:
            return "please enter price"
        if not quantity:
            return "please enter quantity"
        
        item = Item.create(
            item_name=item_name,
            invoice =invoice,
            unit_price=unit_price,
            quantity=quantity,
            amount=amount
        )
        
        return jsonify({
            "item_name": item.item_name,
            "invoice":invoice.invoice_number,
            "unit_price":item.unit_price,
            "quantity":item.quantity,
            "amount":item.amount
        })
    elif request.method == 'PUT':
        try :
            data = request.get_json()
            item = Item.get_by_id(id)
            item.item_name = data.get("item_name")
            invoice_id = data.get("invoice")
            item.invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_id)
            item.unit_price = data.get("unit_price")
            item.quantity = data.get("quantity")

            item.amount = float(item.unit_price) * int(item.quantity)
            return jsonify({
                "id":item.id,
                "item_name": item.item_name,
                "invoice" :item.invoice.invoice_number,
                "unit_price":item.unit_price,
                "quantity":item.quantity,
                "amount":item.amount
            })
        except DoesNotExist:
            return jsonify({
                "message":"Item DoesNotExist"
            })

    elif request.method == "DELETE":
        item = Item.get_by_id(id)
        if not item:
            return jsonify({
                "error":"item not exist"
            })
        item.delete_instance()
        return jsonify({"message":"Item Delete Succussfully"})
    else:
        items = Item.select()
        return jsonify([
            {
                "item_name": item.item_name,
                "invoice": item.invoice.invoice_number,  
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "amount": item.amount
            }
            for item in items
        ])


#weasyprint 
@app.route("/invoices/<string:invoice_number>/pdf", methods=["GET"])
def invoice_pdf(invoice_number):
    try:
        invoice = Invoice.get(Invoice.invoice_number == invoice_number)  
        customer = invoice.customer
        items = Item.select().where(Item.invoice == invoice)

        html = f"""
        <h1>Invoice : {invoice.invoice_number}</h1>
        <p>Customer: {customer.username}</p>
        <p>{customer.email}</p>
        <table border="1">
        <tr><th>Item</th><th>Qty</th><th>Unit Price</th><th>Amount</th></tr>
        """
        for item in items:
            html += f"<tr><td>{item.item_name}</td><td>{item.quantity}</td><td>{item.unit_price}</td><td>{item.amount}</td></tr>"
        html += f"</table><p>Total: ₹{invoice.total_amount}</p>"

        pdf = HTML(string=html).write_pdf()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        return response
    except Invoice.DoesNotExist:
        return jsonify({"error": "Invoice not found"}), 404

@app.route('/')
def home():
    return "hello"



if __name__ == "__main__":
    # print("Creating Model  ")
    app.run(debug=True)