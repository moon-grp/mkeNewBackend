from fastapi import APIRouter, File, UploadFile, Form, Depends
from model.autos.cars import Cars
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import cloudinary as cloud
from cloudinary import uploader as uploadit
from config.adminauth import AuthHandler
load_dotenv()

auto = APIRouter()
auth_handler = AuthHandler()

cloudName = os.getenv("CLOUD_NAME")
clouddApiKey = os.getenv("API_KEY")
cloudApiSecret = os.getenv("API_SECRET")

cloud.config(cloud_name=cloudName,
             api_key=clouddApiKey,
             api_secret=cloudApiSecret)


@auto.get("/viewcars", tags=["admin-autos"])
async def view_car(token: str = Depends(auth_handler.auth_wrapper)):
    thecars = Cars.objects().to_json()
    result = json.loads(thecars)
    return {"cars": result}


@auto.get("/viewcardetails/{id}", tags=["admin-autos"])
async def view_car_details(id, token: str = Depends(auth_handler.auth_wrapper)):
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
async def delete_car(id, token: str = Depends(auth_handler.auth_wrapper)):
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

    file: UploadFile = File(...),
    file2: UploadFile = File(...),
    file3: UploadFile = File(...),
    file4: UploadFile = File(...),
    token: str = Depends(auth_handler.auth_wrapper)

):
    uploadToCloud = uploadit.upload(file.file, )
    getImageUrl = uploadToCloud["url"]
    uploadToCloud2 = uploadit.upload(file2.file, )
    getImageUrl2 = uploadToCloud2["url"]
    uploadToCloud3 = uploadit.upload(file3.file, )
    getImageUrl3 = uploadToCloud3["url"]
    uploadToCloud4 = uploadit.upload(file4.file, )
    getImageUrl4 = uploadToCloud4["url"]

    new_prod = Cars(
        mediaUrl=getImageUrl,
        mediaUrl2=getImageUrl2,
        mediaUrl3=getImageUrl3,
        mediaUrl4=getImageUrl4,
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
                     file: UploadFile = File(...),
                     token: str = Depends(auth_handler.auth_wrapper)):

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
