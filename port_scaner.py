from PyQt5.QtCore import *
from datetime import datetime
from logging import getLogger
import socket


class PortScanner(QThread):
    finished = pyqtSignal(bool)
    progress = pyqtSignal(str)
    progress_count = pyqtSignal(int)

    def __init__(self, target: str, start_point: int, end_point: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.start_point = start_point
        self.end_point = end_point + 1
        self._is_running = True
        self.logger = getLogger('PortScanner')

    def run(self):
        try:
            # target = socket.gethostbyname(self.target)
            self.progress.emit(f"task_start@Start Scan {datetime.today()}")
            self.progress.emit(f'target@Target = <span style="color:cyan;">{self.target}</span>')

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
                self.progress_count.emit(port)
        except KeyboardInterrupt:
            self.progress.emit(f"log@<span style='color:red'>Exiting Program !!!!</span>")
        except socket.gaierror:
            self.progress.emit(f"error@<span style='color:red'>Hostname Could Not Be Resolved !!!!</span>")
        except socket.error:
            self.progress.emit(f"error@<span style='color:red'>Server not responding !!!!</span>")
        except Exception as exception:
            self.progress.emit(f"error@<span style='color:red'>Unknown ERROR check logs </span>")
            self.logger.error(exception)
        finally:
            self.progress_count.emit(0)
            self.logger.info('socket finally finished')
            self.finished.emit(1)

    def stop(self):
        self._is_running = False
