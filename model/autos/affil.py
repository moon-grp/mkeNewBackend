from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField

class affil(Document):
    email = EmailField()
    username = StringField()
    password = IntField()
    date = DateField()