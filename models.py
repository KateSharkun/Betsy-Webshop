from peewee import *

db = SqliteDatabase(':memory:')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True)
    address_data = TextField()
    billing_info = FixedCharField(constraints=[Check("length(billing_info) == 16")], unique=True)

class Tags(BaseModel):
    name = CharField(unique=True)

class Product(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    price = DoubleField()
    quantity = SmallIntegerField()
    tag = ForeignKeyField(Tags, backref='products')
    owner = ForeignKeyField(User, backref='owned_products', null=True)


class Purchases(BaseModel):
    user = ForeignKeyField(User, backref='purchases')
    product = ForeignKeyField(Product, backref='product_bought')
    number_of_purchased_item = SmallIntegerField()




db.connect()
db.create_tables([User, Product, Purchases, Tags])
# Models go here
