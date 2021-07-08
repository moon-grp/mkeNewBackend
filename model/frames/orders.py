from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os
load_dotenv()


uri = os.getenv("Mongo_frame_db")

connect(host=uri, alias="default")



class Orders(Document):
    CustomerName= StringField()
    CustomerEmail = EmailField()
    CustomerPhone = IntField()
    CustomerAddress = StringField()
    Date = DateField()
    ProductName = StringField()
    Quantity = IntField()
    Data = ObjectIdField()
    delivered = BooleanField()


