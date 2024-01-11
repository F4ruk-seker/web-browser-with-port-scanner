from config import API_QUERY_HOST
from bs4 import BeautifulSoup
from camera import detect_face_and_save_image
import requests


def get_bs4_clean_text(obj):
    return obj.text.replace('\n', '').strip()


def get_ip_data() -> dict:
    result = {}
    try:
        response = requests.get(API_QUERY_HOST)
        pyload = BeautifulSoup(response.text, 'html.parser')
        ip_provider = pyload.find('div', {'class': 'query-ip-location-content-info'})
        ip_provider_context = ip_provider.find_all('div')
        result['host'] = get_bs4_clean_text(ip_provider_context[0])
        result['provider'] = get_bs4_clean_text(ip_provider_context[1])
        for frame in pyload.findAll('li'):
            _ = frame.findAll('span')
            result[get_bs4_clean_text(_[1])] = get_bs4_clean_text(_[2])
        return result
    except Exception as err:
        print('ip q err')
        print(err)
    finally:
        return result


def get_user_face_data():
    user_faces = detect_face_and_save_image()
    print("görev tamam ")
    print(user_faces)