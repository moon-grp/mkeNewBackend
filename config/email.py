from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
import smtplib
from dotenv import load_dotenv
load_dotenv()


emailAddress = os.getenv("BASE_EMAIL")
emailPassword = os.getenv("BASE_P")


class Mail():
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

    fm = FastMail(conf)

    async def ordermail(self, mail, name):
        message = MessageSchema(
            subject="Frame Order Notification",
            recipients=[mail],
            body=f"Hi {name}, your order is processing. you should recieve it in 2-3 days.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')

    async def ordernotification(self):
        message = MessageSchema(
            subject="Frame Order",
            recipients=["mrkayenterprise@gmail.com"],
            body=f"New Order just came in check dashboard.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')

    async def affilatenotification (self, mail ,name ,carname, date, num):
        message = MessageSchema(
            subject="Booking inspection notification",
            recipients=[mail],
            body=f"Hi, {name}, your link was used to book inspection of {carname} on ({date}). \nYou can call {num} to follow up on the deal. \nKind Regards.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')

    async def affilatenotificationAdmin (self,name ,carname, date, num):
        message = MessageSchema(
            subject="Booking inspection notification",
            recipients=["mrkayenterprise@gmail.com"],
            body=f"Inspection of {carname} on ({date}) by {name}. \nPhone number:{num}.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')

    async def affilatenotificationUser (self, mail ,name ,carname, date):
        message = MessageSchema(
            subject="Booking inspection notification",
            recipients=[mail],
            body=f"Hi, {name}, you booked inspection of {carname} on ({date}). \nWe would call you shortly to follow up on details. \nKind Regards.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')
