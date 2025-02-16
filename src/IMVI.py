import os
import sys

import cv2
from PyQt5.QtCore import QMimeData, QRect, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QVBoxLayout, QWidget)

from components.frames import Interface
from components.layout import Header
from components.utils import load_fonts

os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts.warning=false"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(800, 400)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = Header(self)
        self.layout.addWidget(self.header)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        conversion_tab = Interface()
        self.tab_widget.addTab(conversion_tab, "Convert Images to Video")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(resource_path("css/style.qss"), 'r') as f:
        app.setStyleSheet(f.read())
    load_fonts("fonts/")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
