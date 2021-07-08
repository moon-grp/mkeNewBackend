from fastapi import APIRouter, File, UploadFile, Form
from model.frames.frames import Frames
import json
from bson.objectid import ObjectId
from pydantic import BaseModel

userFrame = APIRouter()


@userFrame.get("/viewallframes", tags=["users-frames"])
async def view_all_frames():
    product = Frames.objects().to_json()
    fproduct = json.loads(product)
    return {"products": fproduct}



@userFrame.get("/viewframedetails/{id}", tags=["users-frames"])
async def view_frame_details(id):
    prod = Frames.objects.get(id=ObjectId(id))
    Prod_details = {
        "name": prod.productname,
        "price": prod.frameprice,
        "imgurl": prod.imgUrl,
        "description": prod.description,
        "slashprice": prod.slashprice,

    }

    return Prod_details
