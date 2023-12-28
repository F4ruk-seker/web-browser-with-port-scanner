import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ana Pencere")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.button_open_second_window = QPushButton("İkinci Pencereyi Aç")
        self.button_open_second_window.clicked.connect(self.open_second_window)
        self.layout.addWidget(self.button_open_second_window)

        self.central_widget.setLayout(self.layout)

    def open_second_window(self):
        second_window = SecondWindow(self)
        second_window.show()

class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("İkinci Pencere")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QPushButton("Bu İkinci Pencere")
        self.layout.addWidget(self.label)

        self.central_widget.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
