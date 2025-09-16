from flask import Flask
from peewee import *

app = Flask(__name__)
db = SqliteDatabase('invoice.db')

class BaseModel(Model):
    class Meta:
        database = db
    
class Customer(BaseModel):
    id = AutoField(primary_key = True)
    username = CharField(unique=True)
    email = CharField()
    address = TextField()

class Invoice(BaseModel):
    invoice_number = CharField(unique=True)
    customer = ForeignKeyField(Customer, backref="invoices")
    invoice_date = DateField()
    total_amount = FloatField()
    arn_number = CharField(null=True) 

class Item(BaseModel):
    id = AutoField()
    invoice = ForeignKeyField(Invoice, backref="items")
    item_name = CharField(max_length=200)
    quantity = IntegerField()
    unit_price = FloatField()

    @property
    def amount(self):
        return self.quantity * self.unit_price
    

class Users(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    password = TextField()
    

@app.route("/")
def modules():
    return "creating tables"

db.connect()

Customer.create_table()
Invoice.create_table()
Item.create_table()
Users.create_table()
# Item.drop_table()
# Users.drop_table()
# Invoice.drop_table()
# Customer.drop_table()
# print()
if __name__ == "__main__":
    # print("Creating Model  ")
    app.run(debug=True)