from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic.networks import EmailStr
from model.frames.frames import Frames
from model.users.createaccount import Affil
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import cloudinary as cloud
from cloudinary import uploader as uploadit
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()


aff = APIRouter()

passContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Newaccount(BaseModel):
    username: str
    email: str
    password: str

class logIn(BaseModel):
    email: str
    password: str


@aff.post("/signup", tags=["users-affill"])
async def create_account(details: Newaccount):    
    try:
        checkE =  json.loads(Affil.objects.get(email=details.email).to_json())
        raise HTTPException(status_code=400, detail="account already exist..")
    except Affil.DoesNotExist:
        hashPass = passContext.hash(details.password)
        getDetails = Affil(username=details.username,
                       email=details.email,
                       password=hashPass)
        getDetails.save()
        return {"message": "account created..."}




#@aff.post("/signin", tags=["users-affill"])
#async def login_account(details: logIn)
