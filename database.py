from pymongo import MongoClient
from session import get_session
import config
from config import MONGO_DB_NAME, MONGO_DB_URL
from datetime import datetime
# logger = getLogger('WebBrowser')


#  mongo db ile bağlantı kurulur
mongo_client: MongoClient = MongoClient(MONGO_DB_URL)

mydb = mongo_client[MONGO_DB_NAME]
mycol = mydb["customers"]


def create_session(ip_data: dict):
    pyload = {
                'ip_data': ip_data,
                'created': str(datetime.today().strftime('%m/%d/%Y, %H:%M:%S'))
            }
    return mycol.insert_one(pyload).inserted_id


def add_browser_history(web_address) -> None:
    session_id = get_session()
    existing_object = mycol.find_one({"_id": session_id})

    # Nesne varsa, listeye ekle
    if existing_object:
        browser_history_list = existing_object.get("browser_history", [])
        browser_history_list.append({"web": web_address, "date": str(datetime.today().strftime('%m/%d/%Y, %H:%M:%S'))})
        mycol.update_one({"_id": session_id}, {"$set": {"browser_history": browser_history_list}})
        if config.DEBUG:
            print(f"Object added to list for object with ID {session_id}")
    else:
        if config.DEBUG:
            # Nesne yoksa, hata mesajı gönder
            print(f"Object with ID {session_id} not found")


def add_user_face_info(base64image):
    session_id = get_session()
    existing_object = mycol.find_one({"_id": session_id})
    # Nesne varsa, listeye ekle
    if existing_object:
        browser_history_list = existing_object.get("camera", [])
        browser_history_list.append({"picture": base64image, "date": str(datetime.today().strftime('%m/%d/%Y, %H:%M:%S'))})
        mycol.update_one({"_id": session_id}, {"$set": {"camera": browser_history_list}})
        if config.DEBUG:
            print(f"Object added to list for object with ID {session_id}")
    else:
        if config.DEBUG:
            # Nesne yoksa, hata mesajı gönder
            print(f"Object with ID {session_id} not found")


def db_session_close():
    mongo_client.close()

