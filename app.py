from flask import Flask, request,jsonify,make_response, render_template, redirect,url_for
from peewee import *
from modules import * 
from datetime import datetime 
from weasyprint import HTML

app = Flask(__name__)
db = SqliteDatabase('invoice.db')

@app.route('/customer-create')
def customer_create():
    return render_template('customer.html')

@app.route('/customer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def customer():
    if request.method == 'POST':
        data = request.form
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
        customers = Customer.select()
        return render_template('customer-list.html', customers=customers)
    else:
        # customers = Customer.select()
        return render_template('customer.html')
  
@app.route("/customer/<int:id>/update", methods=['POST', 'GET'])
def update_customer(id):
    customer = Customer.get_by_id(id)

    if request.method == "POST":
        customer.username = request.form.get("username")
        customer.email = request.form.get("email")
        customer.address = request.form.get("address")
        customer.save()  
        return redirect(url_for('customer'))  

    return render_template("customer-update"".html", customer=customer)

@app.route("/customer/<int:id>/delete", methods=['GET','POST', "DELETE"])
def delete_update(id):
    
    customer = Customer.get_by_id(id)
    if not customer:
        return "Customer Not Found"
    customer.delete_instance()
    return "Customer Delete"

@app.route("/invoice-create")
def invoice_create():
    items = Item.select()
    return render_template('invoice.html', items=items)

@app.route("/invoice", methods=['POST', 'GET'])
def invoice():
    if request.method == "POST":
        data = request.form
        invoice_number = data.get("invoice_number")
        customer_id = data.get("customer")
        invoice_date = data.get("invoice_date")
        total_amount = data.get("tota_amount")

        item_names = data.getlist("item_name[]")
        qtys = data.getlist("qty[]")
        prices = data.getlist("price[]")

        if not customer_id:
            return "Please enter customer_id"
        if not invoice_number:
            return "Please provide invoice_number"
        if not item_names:
            return "No items added"

        customer = Customer.get_by_id(customer_id)

        # Insert each line item
        for name, qty, price in zip(item_names, qtys, prices):
            Invoice.create(
                invoice_number=invoice_number,
                customer=customer,
                total_amount=total_amount,
                invoice_date=invoice_date,
                item_name=name,
                qty=int(qty),
                price=float(price)
            )

        invoices = Invoice.select()
        return render_template("invoice-list.html", invoices=invoices)

    else:
        invoices = Invoice.select()
        return render_template("invoice-list.html", invoices=invoices)

@app.route("/invoice/<string:invoice_number>/update", methods=['POST','GET'])
def update_invoice(invoice_number):
    invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_number)
    
    if request.method == "POST": 
        # invoice.invoice_number = request.form.get("invoice_number")
        invoice.customer = request.form.get("customer")
        invoice.total_amount = request.form.get("total_amount")
        invoice.create_at = datetime.now()
        invoice.save()

        return redirect(url_for('invoice'))
    # else:
    return render_template('invoice-update.html',invoice=invoice)

@app.route("/invoice/<string:invoice_number>/delete",methods=['GET','POST', 'DELETE'])
def delete_invoice(invoice_number):
    invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_number)
    if not invoice:
        return "invoice_number not found!"
    invoice.delete_instance()
    invoices = Invoice.select()
    return render_template('invoice-list.html', invoices=invoices)

    
@app.route('/item-create')
def item_create():
    return render_template('item.html')

@app.route('/item', methods=['POST', 'GET', 'PUT', 'DELETE'])
def item():
    if request.method == 'POST':
        data = request.form
        item_name = data.get("item_name")
        unit_price = data.get("unit_price")
        quantity = data.get("quantity")
        amount = float(unit_price) * int(quantity)
        
        if not item_name :
            return "please enter item_name"
        if not unit_price:
            return "please enter price"
        if not quantity:
            return "please enter quantity"
        

        Item.create(
            item_name=item_name,
            unit_price=unit_price,
            quantity=quantity,
            amount=amount
        )
        items = Item.select()
        return render_template('item-list.html',items=items)
    items = Item.select()
    return render_template('item-list.html', items=items)        
# return jsonify({
        #     "item_name": item.item_name,
        #     "invoice":invoice.invoice_number,
        #     "unit_price":item.unit_price,
        #     "quantity":item.quantity,
        #     "amount":item.amount
        # })
    # elif request.method == 'PUT':
    #     try :
    #         data = request.get_json()
    #         item = Item.get_by_id(id)
    #         item.item_name = data.get("item_name")
    #         invoice_id = data.get("invoice")
    #         item.invoice = Invoice.get_or_none(Invoice.invoice_number == invoice_id)
    #         item.unit_price = data.get("unit_price")
    #         item.quantity = data.get("quantity")

    #         item.amount = float(item.unit_price) * int(item.quantity)
    #         return jsonify({
    #             "id":item.id,
    #             "item_name": item.item_name,
    #             "invoice" :item.invoice.invoice_number,
    #             "unit_price":item.unit_price,
    #             "quantity":item.quantity,
    #             "amount":item.amount
    #         })
    #     except DoesNotExist:
    #         return jsonify({
    #             "message":"Item DoesNotExist"
    #         })

    # elif request.method == "DELETE":
    #     item = Item.get_by_id(id)
    #     if not item:
    #         return jsonify({
    #             "error":"item not exist"
    #         })
    #     item.delete_instance()
    #     return jsonify({"message":"Item Delete Succussfully"})
    
    # else:
    #     items = Item.select()
    #     return jsonify([
    #         {
    #             "item_name": item.item_name,
    #             "invoice": item.invoice.invoice_number,  
    #             "unit_price": item.unit_price,
    #             "quantity": item.quantity,
    #             "amount": item.amount
    #         }
    #         for item in items
    #     ])


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


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method=="POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        confirmed = data.get("confirmed")

        if not username or username is None:
            return "<script><alert>'must be enter username'</alert></script>"
        if password != confirmed:
            return "password not matched"
        
        users = Users.create(
            username=username,
            password = password
        )
        return render_template('login.html')
    else:
        return render_template("register.html")


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get("username")
        password = data.get("password")

        users = Users.select()
        for user in users:
            if user.username == username and user.password == password:
                return render_template('home.html')
            else:
                return "please enter a correct username and password "
    return render_template('login.html')


@app.route('/')
def home():
    # return render_template("dialog.html")
    return render_template("register.html")




if __name__ == "__main__":
    app.run(debug=True)