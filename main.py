from fastapi import FastAPI
from routes.frame.frameendpoints import frame
from routes.frame.framesusers import userFrame
from routes.frame.frameorders import order
from routes.autos.autosendpoint import auto
from routes.autos.autosuser import userAuto
from routes.users.affilendpoint import aff
from routes.admin.auth import superAdmin
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(frame, prefix="/api/v1/admin")
app.include_router(userFrame, prefix="/api/v1/users")
app.include_router(order, prefix="/api/v1/admin")
app.include_router(auto, prefix="/api/v1/admin")
app.include_router(userAuto, prefix="/api/v1/users")
app.include_router(aff, prefix="/api/v1/users")
app.include_router(superAdmin, prefix="/api/v1/admin")
