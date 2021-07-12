from fastapi import APIRouter, File, UploadFile, Form, Depends
from model.frames.frames import Frames
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import cloudinary as cloud
from cloudinary import uploader as uploadit
import os
from dotenv import load_dotenv
load_dotenv()
from config.adminauth import AuthHandler


auth_handler = AuthHandler()
cloudName = os.getenv("CLOUD_NAME")
clouddApiKey = os.getenv("API_KEY")
cloudApiSecret = os.getenv("API_SECRET")


frame = APIRouter()
cloud.config(cloud_name=cloudName,
             api_key=clouddApiKey,
             api_secret=cloudApiSecret)


@frame.get("/getallproducts", tags=["admin-frames"])
async def get_all_prod(token: str = Depends(auth_handler.auth_wrapper)):
    product = Frames.objects().to_json()
    fproduct = json.loads(product)
    return {"products": fproduct}


@frame.get("/getproduct/{id}", tags=["admin-frames"])
async def get_prod(id, token: str = Depends(auth_handler.auth_wrapper)):
    prod = Frames.objects.get(id=ObjectId(id))
    Prod_details = {
        "name": prod.productname,
        "price": prod.frameprice,
        "imgurl": prod.imgUrl,
        "description": prod.description,
        "slashprice": prod.slashprice,

    }

    return Prod_details


@frame.delete("/deleteproduct/{id}", tags=["admin-frames"])
async def delete_prod(id, token: str = Depends(auth_handler.auth_wrapper)):
    prod = Frames.objects.get(id=ObjectId(id))
    prod.delete()
    return {"message": "Product deleted.."}


class Newframe(BaseModel):
    productname: str
    frameprice: int
    slashprice: int
    description: str


@frame.post("/addproduct", tags=["admin-frames"])
async def add_product(productname: str = Form(...),
                      frameprice: int = Form(...),
                      slashprice: int = Form(...),
                      description: str = Form(...),

                      file: UploadFile = File(...),
                      token: str = Depends(auth_handler.auth_wrapper)):

    uploadToCloud = uploadit.upload(file.file, )
    getImageUrl = uploadToCloud["url"]

    new_prod = Frames(
        imgUrl=getImageUrl,
        available=True,
        productname=productname,
        frameprice=frameprice,
        description=description,
        slashprice=slashprice

    )

    new_prod.save()

    return {"message": "new product created..."}


@frame.post("/updateproduct/{id}", tags=["admin-frames"])
async def update_product(id,
                         productname: str = Form(...),
                         frameprice: int = Form(...),
                         slashprice: int = Form(...),
                         description: str = Form(...),
                         file: UploadFile = File(...),
                         token: str = Depends(auth_handler.auth_wrapper)):

    prod = Frames.objects.get(id=ObjectId(id))

    uploadToCloud = uploadit.upload(file.file, )
    getImageUrl = uploadToCloud["url"]

    prod.update(
        imgUrl=getImageUrl,
        available=True,
        productname=productname,
        frameprice=frameprice,
        description=description,
        slashprice=slashprice

    )

    return {"message": "product updated..."}
