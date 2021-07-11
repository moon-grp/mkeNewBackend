import os
import smtplib
from dotenv import load_dotenv
load_dotenv()


emailAddress = os.getenv("BASE_EMAIL")
emailPassword = os.getenv("BASE_P")


class Sendmail():

    def processMail(self, email):
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.connect()
            smtp.ehlo()
            smtp.starttls()
            smtp.login(emailAddress, emailPassword)

        subject = "Order Processing"
        body = f"Hi, your order is processing. you should recieve it in 2-3 days."

        msg = f'subject:  {subject}\n\n{body}'

        # smtp.sendmail(emailAddress, "gogechi8@gmail.com", msg)
        # smtp.sendmail(emailAddress, cEmail, msg)
        smtp.sendmail(emailAddress, email, msg)
