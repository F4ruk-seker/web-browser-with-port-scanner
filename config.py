from pathlib import Path
import logging


BASE_DIR = Path(__file__).resolve().parent
APP_ICO = BASE_DIR.joinpath('web_browser.ico')


logging.basicConfig(filename='web_browser.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s')
