from flask import Flask
from peewee import *

app = Flask(__name__)
db = SqliteDatabase('invoice.db')

class BaseModel(Model):
    class Meta:
        database = db
    
class Customer(BaseModel):
    id = AutoField(primary_key = True)
    username = CharField()
    email = CharField()
    address = TextField()

class Invoice(BaseModel):
    invoice_number = CharField(unique=True)
    customer = ForeignKeyField(Customer)
    total_amount = FloatField()
    created_at = DateTimeField()
    

class Item(BaseModel):
    id = AutoField()
    item_name = CharField(200)
    invoice = ForeignKeyField(Invoice, backref='items')
    quantity = IntegerField()
    unit_price = FloatField()
    amount = FloatField()



@app.route("/")
def modules():
    return "creating tables"

db.connect()

Customer.create_table()
Invoice.create_table()
Item.create_table()


# print()
if __name__ == "__main__":
    # print("Creating Model  ")
    app.run(debug=True)