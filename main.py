from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from pathlib import Path
from datetime import datetime
import validators

base_url = Path(__file__).resolve().parent

# import nmap
# >>> nm = nmap.PortScanner()


class PortScanner(QThread):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(str)

    def __init__(self, target: str, start_point: int, end_point: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.start_point = start_point
        self.end_point = end_point
        self._is_running = True

    def run(self):
        try:
            import socket
            # target = socket.gethostbyname(self.target)
            try:
                self.progress.emit(f"task_start@Start Scan {datetime.today()}")

                for port in range(self.start_point, self.end_point):
                    if not self._is_running:
                        self.progress.emit("task_termit@Scan cancel")
                        break
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)
                    result = s.connect_ex((self.target, port))
                    if result == 0:
                        self.progress.emit(f"port_found@PORT:({port}):('<span style='color:greenyellow'>GET RESPONSE</span>')")
                    else:
                        self.progress.emit(f"port_not_found@PORT:({port}):('<span style='color:brown'>NO RESPONSE</span>')")
                    s.close()
            except KeyboardInterrupt:
                self.progress.emit(f"log@<span style='color:red'>Exiting Program !!!!</span>")
            except socket.gaierror:
                self.progress.emit(f"error@<span style='color:red'>Hostname Could Not Be Resolved !!!!</span>")
            except socket.error:
                self.progress.emit(f"error@<span style='color:red'>Server not responding !!!!</span>")
            except Exception as exception:
                self.progress.emit(f"error@<span style='color:red'>Unknown ERROR check logs </span>")
                print(exception)
            # Uzun süren işlemlerinizi burada gerçekleştirin

            # for i in range(1, 10):
            #     if not self._is_running:
            #         self.progress.emit("İşlem iptal edildi.")
            #         break
            #
            #     # Simüle edilmiş bir API isteği
            #     self.progress.emit(f"İstek {i} tamamlandı.")
            #     self.msleep(1000)  # 1 saniye bekleme
        except Exception as er:
            print(er)
        finally:
            print('on f')
            self.finished.emit(1)

    def stop(self):
        self._is_running = False


class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)

        self.window = QWidget()
        self.window.setWindowTitle(" Web Browser")
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
        style_sheet = """
        background-color: #181818;
        color: white;
        font-size: 16px;
        font-weight: bold;
        """
        self.setStyleSheet(style_sheet)
        self.window.setStyleSheet(style_sheet)


class PortScanWindow(QMainWindow):
    def __init__(self, parent=None, target: str = 'localhost'):
        super().__init__(parent)
        self.target = target
        min_port_point = 0
        max_port_point = 65_536

        self.setWindowTitle("PORT SCANER")

        self.set_known_ports_btn = QPushButton("KNOWN PORTS")
        self.set_known_ports_btn.setMinimumHeight(30)
        self.set_known_ports_btn.setMaximumHeight(30)
        self.set_known_ports_btn.clicked.connect(self.set_known_ports)

        self.set_all_ports_btn = QPushButton("ALL PORTS")
        self.set_all_ports_btn.setMinimumHeight(30)
        self.set_all_ports_btn.setMaximumHeight(30)
        self.set_all_ports_btn.clicked.connect(self.set_all_ports)

        self.url_bar = QLineEdit()
        self.url_bar.setMinimumHeight(30)
        self.url_bar.setMaximumHeight(30)
        self.url_bar.setMaximumWidth(200)
        self.url_bar.setText(self.target)
        self.url_bar.setPlaceholderText('enter a target')

        start_port_point_validator = QIntValidator()
        start_port_point_validator.setRange(min_port_point, max_port_point - 1)

        self.start_port_point = QLineEdit()
        self.start_port_point.setMinimumHeight(30)
        self.start_port_point.setMaximumHeight(30)
        self.start_port_point.setMinimumWidth(60)
        self.start_port_point.setMaximumWidth(60)
        self.start_port_point.setPlaceholderText('Start Point')
        self.start_port_point.setValidator(start_port_point_validator)
        self.start_port_point.textChanged.connect(self.port_gui_validate)

        end_port_point_validator = QIntValidator()
        end_port_point_validator.setRange(min_port_point, max_port_point)

        self.end_port_point = QLineEdit()
        self.end_port_point.setMinimumHeight(30)
        self.end_port_point.setMaximumHeight(30)
        self.end_port_point.setMinimumWidth(60)
        self.end_port_point.setMaximumWidth(60)
        self.end_port_point.setPlaceholderText('End Point')
        self.end_port_point.setValidator(end_port_point_validator)
        self.end_port_point.textChanged.connect(self.port_gui_validate)

        self.start_scan_btn = QPushButton("START")
        self.start_scan_btn.setMinimumHeight(30)
        self.start_scan_btn.setMaximumHeight(30)
        self.start_scan_btn.clicked.connect(self.start_port_scan)

        self.stop_scan_btn = QPushButton("STOP")
        self.stop_scan_btn.setMinimumHeight(30)
        self.stop_scan_btn.setMaximumHeight(30)
        self.stop_scan_btn.clicked.connect(self.cancel_scan)
        self.stop_scan_btn.setDisabled(True)

        self.app_header = QHBoxLayout()
        self.app_header.addWidget(self.set_known_ports_btn)
        self.app_header.addWidget(self.set_all_ports_btn)
        self.app_header.addWidget(self.url_bar)
        self.app_header.addWidget(self.start_port_point)
        self.app_header.addWidget(self.end_port_point)
        self.app_header.addWidget(self.start_scan_btn)
        self.app_header.addWidget(self.stop_scan_btn)

        self.app_body = QVBoxLayout()

        self.scan_log = QTextEdit()
        self.scan_log.setDisabled(True)
        self.scan_log.setPlaceholderText('Scan Log')

        self.founded_ports_log = QTextEdit()
        self.founded_ports_log.setDisabled(True)
        self.founded_ports_log.setPlaceholderText('Founded Ports Log')

        self.app_body.addWidget(self.scan_log)
        self.app_body.addWidget(self.founded_ports_log)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.app_header)
        self.layout.addLayout(self.app_body)
        # self.window.setLayout(self.horizontal)

        self.label = QPushButton("Bu İkinci Pencere")
        self.layout.addWidget(self.label)

        self.central_widget.setLayout(self.layout)
        self.load_css()
        self.worker_thread = None
        self.set_known_ports()

        '''
        host address bar , scan btn
        scan log
        found log
        '''
    def port_gui_validate(self, *args, **kwargs):
        try:
            start_point = self.start_port_point.text()
            end_point = self.end_port_point.text()
            self.start_port_point.setStyleSheet(f'color:{"white" if 65_535 >= int(start_point) > 0 else "red"}')
            self.end_port_point.setStyleSheet(f'color:{"white" if 65_536 >= int(end_point) > 0 else "red"}')
        except:
            pass

    def set_known_ports(self):
        self.start_port_point.setText('1')
        self.end_port_point.setText('1024')

    def set_all_ports(self):
        self.start_port_point.setText('1')
        self.end_port_point.setText('65536')

    def start_port_scan(self):
        self.start_scan_btn.setDisabled(True)
        self.stop_scan_btn.setDisabled(False)

        self.worker_thread = PortScanner('localhost', int(self.start_port_point.text()), int(self.end_port_point.text()))
        self.worker_thread.finished.connect(self.scan_finished)
        self.worker_thread.progress.connect(self.update_status)
        self.worker_thread.start()

    def cancel_scan(self):
        if self.worker_thread:
            self.worker_thread.stop()

    def scan_finished(self, *args, **kwargs):
        self.start_scan_btn.setDisabled(False)
        self.stop_scan_btn.setDisabled(True)
        self.label.setText("Durum: İşlem tamamlandı")

    def update_status(self, status):
        status = status.split('@')
        status_type = status[0]
        status_message = status[1]
        print(f'"{status_type}"')
        if status_type == 'port_found':
            print('girdi port_found')

            self.founded_ports_log.append(status_message)
        self.scan_log.append(status_message)
        self.label.setText(f"Durum: {status_message}")

    def load_css(self):
        style_sheet = """
        *{
        background-color: #181818;
        color: white;
        font-size: 16px;
        font-weight: bold;
        }
        QPushButton:disabled{
        color:red
        }
        """
        self.setStyleSheet(style_sheet)
        # self.window.setStyleSheet(style_sheet)

try:
    app = QApplication([])
    window = MyWebBrowser()
    # window = PortScanWindow()
    # window.show()
    ico = base_url.joinpath('web_browser.ico')
    window.window.setWindowIcon(QIcon(str(ico)))
    app.exec_()
except Exception as err:
    print(err)


