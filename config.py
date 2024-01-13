from pathlib import Path
import logging
import os

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
DEBUG: bool = True

#  debug True iken camera modeli için buradaki adresi kullanır , isterseniz mp4 dosyaı ile de test edebilirsiniz
TEST_VIDEO_SOURCE: str = 'test_objects/IRONMAN 4 – Official Trailer.mp4'
# TEST_VIDEO_SOURCE: str = 'http://192.168.0.102:8080/video'

#  tarayıcnın görünümü için css dosyasını okur ve işaretler
with open('style.css', 'r') as __css_ref:
    APP_CSS: str = __css_ref.read()

#  session ID başta None(null) dır main den start verilince mongo db den id atanır
#  ve diğer backdoor datası bu id üzerne kayıt edilir
SESSION_ID: str | None = None


class BROWSER:
    """
    çoklu çekirdek programlamada deneyimim az o yüzden backdoor serverisleri için buludğum
    en uygun sync yöntemi dosya yazma oldu
    """

    # class bağımsız çalışması için static
    @staticmethod
    def is_stop() -> bool:
        # dosyayı okumda modunda, oku ve 1 e eşit mi söyle
        with open('real_time_sync', 'r', encoding='utf-8') as real_time_sync:
            # okuann değer bir değişkene atanıyor ve string ifade ile karşılaştırlıyor
            context = real_time_sync.read()
            return str(context) == '1'

    # class bağımsız çalışması için static
    @staticmethod
    def start():
        #  dosyayı yazma modunda aç önceki değeri siler bu mod ve 0 yaz
        #  tarayıcı durdu mu sorusuna 0 yani hayır der
        with open('real_time_sync', 'w', encoding='utf-8') as real_time_sync:
            real_time_sync.write('0')

    # class bağımsız çalışması için static
    @staticmethod
    def stop():
        #  dosyayı yazma modunda aç önceki değeri siler bu mod ve 1 yaz
        #  tarayıcı durdu mu sorusuna 1 yani evet der
        with open('real_time_sync', 'w', encoding='utf-8') as real_time_sync:
            real_time_sync.write('1')


