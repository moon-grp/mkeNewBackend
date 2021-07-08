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

auto = APIRouter()

cloudName = os.getenv("CLOUD_NAME")
clouddApiKey = os.getenv("API_KEY")
cloudApiSecret = os.getenv("API_SECRET")

cloud.config(cloud_name=cloudName,
             api_key=clouddApiKey,
             api_secret=cloudApiSecret)


@auto.get("/viewcars", tags=["admin-autos"])
async def view_car():
    thecars = Cars.objects().to_json()
    result = json.loads(thecars)
    return {"cars": result}


@auto.get("/viewcardetails/{id}", tags=["admin-autos"])
async def view_car_details(id):
    getCar = Cars.objects.get(id=ObjectId(id))
    carDetails = {
        "carname": getCar.carname,
        "carprice": getCar.carprice,
        "description": getCar.description,
        "location": getCar.location,
        "available": getCar.available,
        "mediaUrl": getCar.mediaUrl,
        "commission": getCar.commission
    }
    return carDetails


@auto.delete("/deletecar/{id}", tags=["admin-autos"])
async def delete_car(id):
    getCar = Cars.objects.get(id=ObjectId(id))
    getCar.delete()
    return{"message": "car deleted"}


@auto.post("/createpost", tags=["admin-autos"])
async def create_post(
    carname: str = Form(...),
    carprice: int = Form(...),
    description: str = Form(...),
    commission: str = Form(...),
    location: str = Form(...),

    file: UploadFile = File(...)
):
    uploadToCloud = uploadit.upload(file.file, )
    getImageUrl = uploadToCloud["url"]

    new_prod = Cars(
        mediaUrl=getImageUrl,
        available=True,
        carname=carname,
        carprice=carprice,
        description=description,
        commission=commission,
        location=location
    )

    new_prod.save()

    return {"message": "new product created..."}


@auto.post("/updatedcar/{id}", tags=["admin-autos"])
async def update_car(id,
                     carname: str = Form(...),
                     carprice: int = Form(...),
                     description: str = Form(...),
                     commission: str = Form(...),
                     location: str = Form(...),
                     file: UploadFile = File(...)):

    getCar = Cars.objects.get(id=ObjectId(id))
    uploadToCloud = uploadit.upload(file.file, )
    getImageUrl = uploadToCloud["url"]

    getCar.update(
        mediaUrl=getImageUrl,
        available=True,
        carname=carname,
        carprice=carprice,
        description=description,
        commission=commission,
        location=location
    )

    return {"message": "car updated..."}
