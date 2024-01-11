from pymongo import MongoClient
import config


mongo_client: MongoClient = MongoClient(config.MONGO_DB_URL)
# mydb = mongo_client[config.MONGO_DB_NAME]

mydb = mongo_client["mydatabase"]
mycol = mydb["customers"]

mydict = {"name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)
