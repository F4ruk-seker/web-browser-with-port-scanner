from pathlib import Path
import logging


BASE_DIR = Path(__file__).resolve().parent
APP_ICO = BASE_DIR.joinpath('web_browser.ico')

BROWSER_NAME: str = 'pars'

logging.basicConfig(filename='web_browser.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s')

DEBUG: bool = True

with open('style.css', 'r') as __css_ref:
    APP_CSS: str = __css_ref.read()

