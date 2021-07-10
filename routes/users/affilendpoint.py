from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
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
import validators
from config.auth import AuthHandler
load_dotenv()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
aff = APIRouter()
auth_handler = AuthHandler()
#passContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
#token_secret = os.getenv("JWT_aff_KEY")
#token_algorithm = "HS256"


class Newaccount(BaseModel):
    username: str
    email: str
    password: str


class logIn(BaseModel):
    email: str
    password: str


"""""
def create_token(data: dict, expire_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    encodeJwt = jwt.encode(to_encode, token_secret, algorithm=token_algorithm)
    return encodeJwt
"""""


@aff.post("/signup", tags=["users-affill"])
async def create_account(details: Newaccount, token: str = Depends(auth_handler.auth_wrapper)):
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
