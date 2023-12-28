from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import config
from view import MyWebBrowser
from logging import getLogger

logger = getLogger('WebBrowser')

try:
    app = QApplication([])
    window = MyWebBrowser()
    ico = config.APP_ICO
    window.window.setWindowIcon(QIcon(str(ico)))
    app.exec_()
except Exception as exception:
    logger.error(exception)


