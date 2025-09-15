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
    customer = ForeignKeyField(Customer)
    invoice_date = DateField()
    item_name = CharField()
    qty = IntegerField()
    price = FloatField()
    total_amount = FloatField()

    

class Item(BaseModel):
    id = AutoField()
    item_name = CharField(200)
    quantity = IntegerField()
    unit_price = FloatField()
    # amount = FloatField()

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
# Users.create_table()
# Item.drop_table()
# Users.drop_table()
# Invoice.drop_table()
# Customer.drop_table()
# print()
if __name__ == "__main__":
    # print("Creating Model  ")
    app.run(debug=True)