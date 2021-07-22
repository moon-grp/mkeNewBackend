from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from mongoengine.fields import DictField

class Booking(Document):
    email = EmailField()
    ref = StringField()
    phoneNumber = IntField()
    date = StringField()
    name = StringField()
    actionOncar = BooleanField()
    transData = DictField()
    carName = StringField()