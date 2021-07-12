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

    async def ordermail(self, mail , name):
        message = MessageSchema(
            subject="Frame Order",
            recipients=[mail],
            body=f"Hi {name}, your order is processing. you should recieve it in 2-3 days.",
            subtype="html"
        )
        await self.fm.send_message(message, template_name='email.html')
