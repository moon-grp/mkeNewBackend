from fastapi import APIRouter, File, UploadFile, Form
from model.frames.orders import Orders
import json
from bson.objectid import ObjectId
from pydantic import BaseModel


order = APIRouter()

@order.get("/vieworders", tags=["admin-frames-orders"])
async def view_order():
    theorder = Orders.objects().to_json()
    result = json.loads(theorder)
    return {"orders": result}