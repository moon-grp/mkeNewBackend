from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from mongoengine import connect, disconnect
from dotenv import load_dotenv
import os
load_dotenv()


uri = os.getenv("Mongo_frame_db")


connect(host=uri)


class Cars(Document):
    carname = StringField()
    carprice = IntField()
    available = BooleanField()
    description = StringField()
    commission = DecimalField()
    mediaUrl = URLField()
    mediaUrl2 = URLField()
    mediaUrl3 = URLField()
    mediaUrl4 = URLField()
    slug = StringField()
    location = StringField()
    year = StringField()
    mileage = StringField()
    transmission = StringField()
    color = StringField()
    condition = StringField()
