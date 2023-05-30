# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"
import models
from models import *
from peewee import *
import sys
#from spellchecker import SpellChecker
# Add your code after this line


def search(term):
    #database is not used further so for the convenience function returns list of names
 #   spell = SpellChecker(distance=2)
  #  term = spell.correction(term)
    print(term)
    products_list = [product.name for product in Product.select().where(Product.name.contains(term) | Product.description.contains(term))]
    if len(products_list) == 0:
        print('Item not found')
    else:
        return products_list

def list_user_products(user_id):
    return [product.name for product in Product.select().join(User).where(Product.owner.id == user_id)]


def list_products_per_tag(tag_id):
    return [i.name for i in models.Product.select().where(models.Product.tag_id == tag_id)]


def add_product_to_catalog(user_id, product):
    #Assuming that product argument comes as Product object we are checking if it already has an owner
    if product.owner == None:
        product.update(owner=models.User.get_by_id(user_id))
    else:
        print(f'Product belongs to {product.owner.name}')

def update_stock(product_id, new_quantity):
    try:
        with db.atomic():
            product = Product.update(quantity=new_quantity).where(Product.id == product_id)
            product.execute()
            print('done')
    except IntegrityError:
        print('Product is not in database. You can add it using add_product_to_catalog function')


def purchase_product(product_id, buyer_id, quantity):#done

    try:
        with db.atomic() as transaction:
            #creating a purchase
            try:
                buyer = models.User.get_by_id(buyer_id)
            except Exception:
                print('User not found')
                transaction.rollback()
            try:
                product = models.Product.get_by_id(product_id)
            except Exception:
                print('Product not found')
                transaction.rollback()
            if buyer.id == product.owner.id:
                print('You can`t buy your own products')
                transaction.rollback()
            Purchases.get_or_create(user=buyer, product=product, number_of_purchased_item=quantity)
            present_in_stock = Product.get(Product.name == product.name)


            if present_in_stock.quantity < quantity:
                print(f'Not enough {product.name} items in stock')
                transaction.rollback()
            else:
                Product.update(quantity=Product.quantity-quantity).where(Product.id == product_id).execute()
                if product.quantity == 0:
                    remove_product(product_id)


    except ValueError:
        transaction.rollback()




def remove_product(product_id):
    try:
        product = Product.get_by_id(product_id)
        product.delete_instance()
        print('Done')
    except Exception:
        print('No such product in database')
#done

def populate_test_database():
    clothes = Tags.create(name ='clothes')
    food = Tags.create(name ='food')
    accessoires = Tags.create(name ='accessoires')
    users = [{"name": 'Christiaan', "address_data": 'Labradorstroom 75', "billing_info": '1234567890123451'},
             {"name": 'Jeannot', "address_data": 'Hroshko 75', "billing_info": '1234567890123456'},
             {"name": 'Hans', "address_data": 'Zuiderzee 13', "billing_info": '1234567890123452'},
             {"name": 'Stefan', "address_data": 'Inkommen 2', "billing_info": '1234567890123434'}
             ]
    with db.atomic():
        for data_dict in users:
            User.create(**data_dict)
    data_source = [{"name":'pie', "description":'sweet fruit pies', "price":0.9, "quantity":3, 'tag': food, 'owner':models.User.select().where(models.User.name=='Christiaan')},
                   {"name":'apple', "description":'red apples', "price":0.3, "quantity":30, 'tag':food, 'owner':models.User.select().where(models.User.name=='Jeannot')},
                   {"name":'hat', "description":'black fedoras', "price":1, "quantity":12,'tag':accessoires, 'owner':models.User.select().where(models.User.name=='Jeannot')},
                   {"name":'coat', "description":'furry coat', "price":12, "quantity":3, 'tag':clothes,'owner':models.User.select().where(models.User.name=='Christiaan') },
                   {"name":'pants', "description":'jeans pants', "price":1.5, "quantity":8, 'tag':clothes, 'owner':models.User.select().where(models.User.name=='Hans')}]
    with db.atomic():
        for data_dict in data_source:
            Product.create(**data_dict)


populate_test_database()

