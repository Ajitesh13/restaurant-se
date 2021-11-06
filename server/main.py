from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import db
import json
from model import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    print("Hello World")
    return {"msg": "hello world"}


@app.post("/api/add_item")
async def add_item(item: Item):
    try:
        database = db.client.Restaurant.item_list
        name = item.__dict__['name']
        data = database.find_one({"name": name})
        if data == None:
            database.insert_one(item.__dict__)
        else:
            database.update_one(
                {"name": name}, {"$set": {"quantity": data['quantity'] + item.__dict__['quantity']}})
    except:
        print("Couldn't Insert Data")


@app.get("/api/get_item")
async def get_item():
    database = db.client.Restaurant.item_list
    data_arr = database.find()
    for x in data_arr:
        print(x)
    return []
