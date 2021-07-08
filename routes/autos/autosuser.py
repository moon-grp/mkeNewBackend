from fastapi import APIRouter, File, UploadFile, Form
from model.autos.cars import Cars
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import cloudinary as cloud
from cloudinary import uploader as uploadit
load_dotenv()

userAuto = APIRouter()

cloudName = os.getenv("CLOUD_NAME")
clouddApiKey = os.getenv("API_KEY")
cloudApiSecret = os.getenv("API_SECRET")

cloud.config(cloud_name=cloudName,
             api_key=clouddApiKey,
             api_secret=cloudApiSecret)


@userAuto.get("/getcars", tags=["users-autos"])
async def get_cars():
    getCars = Cars.objects().to_json()
    result = json.loads(getCars)
    return {"cars":result}

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

