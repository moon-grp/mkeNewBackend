from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from mongoengine import connect,disconnect
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
    slug = StringField()
    location = StringField()
    
