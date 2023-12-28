import validators
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from .port_scanner_view import PortScanWindow
import config


class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)

        self.window = QWidget()
        self.window.setWindowTitle(config.BROWSER_NAME)
        self.browser = QWebEngineView()

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        # horizontal > layout
        self.url_bar = QTextEdit()
        self.url_bar.setMinimumHeight(30)
        self.url_bar.setMaximumHeight(30)

        self.go_btn = QPushButton("GO")
        self.go_btn.setMinimumHeight(30)
        self.go_btn.setMaximumHeight(30)

        self.go_main_page_btn = QPushButton("HOME")
        self.go_main_page_btn.setMinimumHeight(30)
        self.go_main_page_btn.setMaximumHeight(30)

        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setMaximumHeight(30)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setMaximumHeight(30)

        self.open_port_scanner_btn = QPushButton("port scan")
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setMaximumHeight(30)

        #  horizontal > layout - collect
        self.horizontal.addWidget(self.go_main_page_btn)
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.open_port_scanner_btn)

        #  horizontal > layout - functions
        #  yatay üst menü fonksiyon bağlantıları
        self.go_main_page_btn.clicked.connect(self.go_home_page)
        self.go_btn.clicked.connect(self.trigger_go_btn)

        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.open_port_scanner_btn.clicked.connect(self.open_port_scanner)

        self.browser.urlChanged.connect(self.url_change)


        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.window.setLayout(self.horizontal)

        self.go_home_page()
        self.window.setLayout(self.layout)
        self.window.show()
        self.load_css()

    def url_change(self, url):
        self.url_bar.setText(url.toString())

    def trigger_go_btn(self, *args, **kwargs):
        url = self.url_bar.toPlainText()
        if not validators.url(url):  # eğer girdi url değil ise
            if validators.url('https://' + url):  # eğer girdi https eklendipinde url ise
                url = 'https://' + url
            else:  # değil ise boşlukları + ile birleştir ve arama yap
                url = f'https://duckduckgo.com/?q={url.replace(" ", "+")}'
        # self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

    def go_home_page(self):
        self.browser.setUrl(QUrl("https://duckduckgo.com/"))

    def open_port_scanner(self):
        from urllib.parse import urlparse

        url = self.url_bar.toPlainText()
        url = urlparse(url)
        port_scan_window = PortScanWindow(self, target=url.hostname)
        port_scan_window.show()

    def load_css(self):
        self.setStyleSheet(config.APP_CSS)
        self.window.setStyleSheet(config.APP_CSS)
