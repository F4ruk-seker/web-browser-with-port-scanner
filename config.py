from pathlib import Path
import logging
import os

MONGO_DB_URL: str = os.getenv('MONGO_DB_URL')
MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME')

BASE_DIR = Path(__file__).resolve().parent
APP_ICO = BASE_DIR.joinpath('web_browser.ico')

BROWSER_NAME: str = 'pars'

logging.basicConfig(filename='web_browser.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s')

DEBUG: bool = True

TEST_VIDEO_SOURCE: str = 'http://192.168.0.102:8080/video'

with open('style.css', 'r') as __css_ref:
    APP_CSS: str = __css_ref.read()

