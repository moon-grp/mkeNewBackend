from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from model.autos.cars import Cars
from model.autos.bookings import Booking
from model.users.createaccount import Affil
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import cloudinary as cloud
from cloudinary import uploader as uploadit
from config.email import Mail
emailhandler = Mail()
load_dotenv()

userAuto = APIRouter()

paystack = os.getenv("pAPI_KEY")

cloudName = os.getenv("CLOUD_NAME")
clouddApiKey = os.getenv("API_KEY")
cloudApiSecret = os.getenv("API_SECRET")

cloud.config(cloud_name=cloudName,
             api_key=clouddApiKey,
             api_secret=cloudApiSecret)


class Bookit(BaseModel):
    email: str
    name: str
    phone: int
    ref: str
    date: str
    referenceCode: str
    carName: str


@userAuto.get("/getcars", tags=["users-autos"])
async def get_cars():
    getCars = Cars.objects().to_json()
    result = json.loads(getCars)
    return {"cars": result}


@userAuto.get("/getcar/{id}", tags=["users-autos"])
async def get_car(id):
    getCar = Cars.objects.get(id=ObjectId(id))
    carDetails = {
        "carname": getCar.carname,
        "carprice": getCar.carprice,
        "description": getCar.description,
        "location": getCar.location,
        "mediaUrl": getCar.mediaUrl,
    }
    return carDetails


@userAuto.post("/bookings", tags=["users-autos"])
async def booking(details: Bookit):
    referenceCode = details.referenceCode

    verifyPayments = requests.get(f"https://api.paystack.co/transaction/verify/{referenceCode}",  headers={
        'Authorization': f'Bearer {paystack}'})

    data = json.loads(verifyPayments.content)

    if details.ref == "undefined":
        addBooking = Booking(
            carName= details.carName,
            email=details.email,
            name=details.name,
            phoneNumber=details.phone,
            ref="no referee",
            date=details.date,
            actionOncar=False,
            transData = data
        )

        addBooking.save()

        return{"message": "Date booked..."}
    else:
        try:

            checkE = json.loads(Affil.objects.get(username=details.ref).to_json())
            email = checkE["email"]
            addBooking = Booking(
            carName= details.carName,
            email=details.email,
            name=details.name,
            phoneNumber=details.phone,
            ref=details.ref,
            date=details.date,
            actionOncar=False,
            transData = data
        )

            addBooking.save()
            await emailhandler.affilatenotification(email, details.ref, details.carName, details.date, details.phone)

            return{"message": "Date booked..."}
        except:
            raise HTTPException(status_code=400, detail="Invalid referee")

        
    

    
