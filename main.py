from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient
from bson.objectid import ObjectId

import os


mongo_client: MongoClient = MongoClient(os.getenv('MONGO_DB_URL'))
mydb = mongo_client[os.getenv('MONGO_DB_NAME')]
mycol = mydb["customers"]


app = FastAPI()
origins = os.getenv('allow_origins').split(" ")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return [{'id': str(x.get('_id')), 'ip_data': x.get('ip_data')} for x in mycol.find({})]


@app.get("/get/{_id}/")
async def get_data(_id: str):
    obj = mycol.find_one({'_id': ObjectId(_id)})
    obj['_id'] = str(obj['_id'])
    return obj
