from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os

from mongoengine.fields import DictField
load_dotenv()


uri = os.getenv("Mongo_frame_db")

connect(host=uri, alias="default")



class Orders(Document):
    CustomerName= StringField()
    CustomerEmail = EmailField()
    CustomerPhone = IntField()
    CustomerAddress = StringField()
    Date = StringField()
    ProductName = StringField()
    Quantity = IntField()
    Data = DictField()
    delivered = BooleanField()


