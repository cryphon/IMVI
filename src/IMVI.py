import os
import sys

import cv2
from PyQt5.QtCore import QMimeData, QRect, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QVBoxLayout, QWidget)

from header import CustomHeader
from interface import Interface
from list_widget import ListWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(400, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create a container widget to hold both header and content
        self.container = QWidget()
        self.setCentralWidget(self.container)

        # Create a vertical layout for the container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Add the custom header
        self.header = CustomHeader(self)
        self.layout.addWidget(self.header)

        # Create and add the tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Add your conversion tab
        conversion_tab = Interface()
        self.tab_widget.addTab(conversion_tab, "Convert Images to Video")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss = "css/style.qss"
    if os.path.exists(qss):
        with open(qss, "r") as fh:
            app.setStyleSheet(fh.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
