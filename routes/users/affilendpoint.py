from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from pydantic.networks import EmailStr
from model.frames.frames import Frames
from model.users.createaccount import Affil
from model.autos.cars import Cars
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import cloudinary as cloud
from cloudinary import uploader as uploadit
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
import validators
from config.auth import AuthHandler
load_dotenv()


aff = APIRouter()
auth_handler = AuthHandler()



class Newaccount(BaseModel):
    username: str
    email: str
    password: str


class logIn(BaseModel):
    email: str
    password: str


@aff.post("/signup", tags=["users-affill"])
async def create_account(details: Newaccount):
    if validators.email(details.email) != True:
        raise HTTPException(status_code=400, detail="email not valid..")

    try:
        checkE = json.loads(Affil.objects.get(email=details.email).to_json())
        raise HTTPException(status_code=400, detail="account already exist..")
    except Affil.DoesNotExist:
        hashPass = auth_handler.get_password_hash(details.password)
        getDetails = Affil(username=details.username,
                           email=details.email,
                           password=hashPass)
        getDetails.save()
        token = auth_handler.encode_token(details.email)
        return {"message": "account created...", "token": token}


@aff.post("/signin", tags=["users-affill"])
async def login_account(details: logIn):
    email = details.email
    password = details.password
    try:
        checkE = json.loads(Affil.objects.get(email=email).to_json())
        passwordCheck = auth_handler.verify_password(
            password, checkE["password"])
        if passwordCheck:
            token = auth_handler.encode_token(email)

            return{"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=400, detail="invalid email or password")

    except Affil.DoesNotExist:
        raise HTTPException(
            status_code=400, detail="invalid email or password")


@aff.get("/affiliate/viewcardetails/{id}", tags=["users-affill"])
async def aff_view_details(id, token: str = Depends(auth_handler.auth_wrapper)):
    try:
        checkE = json.loads(Affil.objects.get(email=token).to_json())
        username = checkE["username"]
        querylink = f"http://localhost:3000/autos/affiliates/garage/{ObjectId(id)}?ref={username}"
        getCar = Cars.objects.get(id=ObjectId(id))
        carDetails = {
            "carname": getCar.carname,
            "carprice": getCar.carprice,
            "description": getCar.description,
            "location": getCar.location,
            "available": getCar.available,
            "mediaUrl": getCar.mediaUrl,
            "commission": getCar.commission,
            "refLink": querylink
        }
        return carDetails
    except:
        raise HTTPException(status_code=401, detail="unauthorized")
