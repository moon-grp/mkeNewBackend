from datetime import date
from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.fields import DecimalField, StringField, URLField, BooleanField, Document, IntField, EmailField, DateField
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os
load_dotenv()


uri = os.getenv("Mongo_frame_db")

connect(host=uri, alias="default")



class Affil(Document):
    email= EmailField()
    username = StringField()
    password = StringField()
    date = DateField()
    userProfile = ObjectIdField()
