
from mongoengine import Document
from mongoengine.fields import DecimalField, StringField, URLField, BooleanField, Document, IntField
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os
load_dotenv()


uri = os.getenv("Mongo_frame_db")

connect(host=uri, alias="default")


class Frames(Document):
    productname = StringField()
    frameprice = IntField()
    available = BooleanField()
    imgUrl = URLField()
    slashprice = IntField()
    slug = StringField()
    description = StringField()


