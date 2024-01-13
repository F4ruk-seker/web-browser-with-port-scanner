from config import API_QUERY_HOST

from bs4 import BeautifulSoup
from camera import detect_face_and_save_image
import requests


def get_bs4_clean_text(obj):
    #  gelen nesenenin text ifadesindeki boşluk karaterlerini siler
    return obj.text.replace('\n', '').strip()


def get_ip_data() -> dict:
    #  sonuç
    result = {}
    try:
        #  ip query servisine istemciden istek atıp ıp ve diğer bilgilerini alıyoruz
        response = requests.get(API_QUERY_HOST)
        print(f"response status code{response}")
        print(f"response status code{response.status_code}")
        #  gelen html datasını parçalıyoruz
        pyload = BeautifulSoup(response.text, 'html.parser')
        #  ip_provider farklı bir html objesinden alıyoruz
        ip_provider = pyload.find('div', {'class': 'query-ip-location-content-info'})
        #  ip_provider ın aldında div listesinden sağlayıcı bilgilerini alıyoruz
        ip_provider_context = ip_provider.find_all('div')
        #  result:host ip adresimiz
        result['host'] = get_bs4_clean_text(ip_provider_context[0])
        #  result:provider internet sağlayıcımz
        result['provider'] = get_bs4_clean_text(ip_provider_context[1])
        #  diğer meta bilgilerini > li etiketi taşıyan list elemanlarınıdan alıp key ve value şeklinde alıyoruz
        #  [key]=value
        for frame in pyload.findAll('li'):
            _ = frame.findAll('span')
            result[get_bs4_clean_text(_[1])] = get_bs4_clean_text(_[2])
    #  eğer hata alırsak logluyoruz
    except Exception as exception:
        # $ log yazılacak
        print(exception)
    finally:
        #  sonuçları return ediyoruz
        return result


def get_user_face_data():
    detect_face_and_save_image()

