from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
from port_scaner import PortScanner


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
        self.set_known_ports_btn.setMaximumWidth(150)
        self.set_known_ports_btn.clicked.connect(self.set_known_ports)

        self.set_all_ports_btn = QPushButton("ALL PORTS")
        self.set_all_ports_btn.setMinimumHeight(30)
        self.set_all_ports_btn.setMaximumHeight(30)
        self.set_all_ports_btn.setMaximumWidth(140)
        self.set_all_ports_btn.clicked.connect(self.set_all_ports)

        self.url_bar = QLineEdit()
        self.url_bar.setMinimumHeight(30)
        self.url_bar.setMaximumHeight(30)
        # self.url_bar.setMaximumWidth(200)
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
        self.start_scan_btn.setMaximumWidth(100)
        self.start_scan_btn.clicked.connect(self.start_port_scan)

        self.stop_scan_btn = QPushButton("STOP")
        self.stop_scan_btn.setMinimumHeight(30)
        self.stop_scan_btn.setMaximumHeight(30)
        self.stop_scan_btn.setMaximumWidth(100)
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

        self.scan_progress_bar = QProgressBar()
        self.scan_progress_bar.setMinimumHeight(20)
        self.scan_progress_bar.setMaximumHeight(20)

        self.app_body.addWidget(self.scan_log)
        self.app_body.addWidget(self.founded_ports_log)
        self.app_body.addWidget(self.scan_progress_bar)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.app_header)
        self.layout.addLayout(self.app_body)
        # self.window.setLayout(self.horizontal)

        self.label = QTextEdit()
        self.label.setDisabled(True)
        self.label.setMinimumHeight(30)
        self.label.setMaximumHeight(30)
        self.label.setPlaceholderText('Durum :')
        self.label.setStyleSheet("text-align: center")

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

    def update_scan_progress_status(self, status: int):
        self.scan_progress_bar.setValue(status)

    def start_port_scan(self):
        self.start_scan_btn.setDisabled(True)
        self.stop_scan_btn.setDisabled(False)

        self.scan_progress_bar.setRange(int(self.start_port_point.text()), int(self.end_port_point.text()))

        self.worker_thread = PortScanner(self.target, int(self.start_port_point.text()), int(self.end_port_point.text()))
        self.worker_thread.finished.connect(self.scan_finished)
        self.worker_thread.progress.connect(self.update_status)
        self.worker_thread.progress_count.connect(self.update_scan_progress_status)
        self.worker_thread.start()

    def cancel_scan(self):
        if self.worker_thread:
            self.worker_thread.stop()

    def scan_finished(self, *args, **kwargs):
        self.update_scan_progress_status(0)
        self.start_scan_btn.setDisabled(False)
        self.stop_scan_btn.setDisabled(True)
        self.label.setText("Durum: İşlem tamamlandı")

    def update_status(self, status):
        status = status.split('@')
        status_type = status[0]
        status_message = status[1]
        if status_type == 'port_found':
            self.founded_ports_log.append(status_message)
        self.scan_log.append(status_message)
        self.label.setText(f"Durum: {status_message}")

    def load_css(self):
        self.setStyleSheet(config.APP_CSS)
        # self.window.setStyleSheet(style_sheet)
