from config.email import Mail
from fastapi import APIRouter, File, UploadFile, Form
from model.frames.orders import Orders
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

order = APIRouter()
paystack = os.getenv("pAPI_KEY")
emailhandler = Mail()

emailAddress = os.getenv("BASE_EMAIL")
emailPassword = os.getenv("BASE_P")


conf = ConnectionConfig(
   MAIL_USERNAME=emailAddress,
   MAIL_PASSWORD=emailPassword,
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_TLS=True,
   MAIL_SSL=False,
   MAIL_FROM=emailAddress,
   MAIL_FROM_NAME="Mr kay enterprise",
   TEMPLATE_FOLDER='./templates'
)

template = """
        <html>
        <body>
          
<p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
  
        </body>
        </html>
        """

message = MessageSchema(
       subject="Fastapi-Mail module",
       recipients=["olumidemm@gmail.com"],
       body= "ol",
       subtype="html"
       )

class Payframe(BaseModel):
    CustomerName: str
    CustomerEmail: str
    CustomerPhone: str
    CustomerAddress: str
    ProductName: str
    Quantity: int
    referenceCode: str


@order.get("/vieworders", tags=["admin-frames-orders"])
async def view_order():
    theorder = Orders.objects().to_json()
    result = json.loads(theorder)
    return {"orders": result}


@order.post("/payforframe", tags=["users-frames-pay"])
async def pay_for_frame(details: Payframe):
    referenceCode = details.referenceCode

    verifyPayments = requests.get(f"https://api.paystack.co/transaction/verify/{referenceCode}",  headers={
        'Authorization': f'Bearer {paystack}'})

    data = json.loads(verifyPayments.content)
    transDate = data["data"]["transaction_date"]
    dateTostring = str(transDate)

    theorder = Orders(
        CustomerName=details.CustomerName,
        CustomerEmail=details.CustomerEmail,
        CustomerPhone=details.CustomerPhone,
        CustomerAddress=details.CustomerAddress,
        Date=dateTostring,
        ProductName=details.ProductName,
        Quantity=details.Quantity,
        Data=data,
        delivered=False
    )

    theorder.save()

    return {"message": "transaction successful..."}


@order.post("/processorder/{id}", tags=["admin-frames-orders"])
async def process_order(id):

    getprod = Orders.objects.get(id=ObjectId(id))
    getprod.update(
        delivered=True
    )
    getemail = getprod["CustomerEmail"]
    getname = getprod["CustomerName"]

    #fm = FastMail(conf)
    await emailhandler.ordermail(getemail, getname)
    #await fm.send_message(message, template_name='email.html')

    return {"message": "customer notified..."}
