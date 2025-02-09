import os
import sys

import cv2
from PyQt5.QtCore import QMimeData, QRect, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

from interface import Interface
from list_widget import ListWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Image to Video Converter")
        self.setMinimumSize(400, 600)  # Smaller window size
        self._create_ui()

    def _create_ui(self):
        # Create a tabbed interface
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        conversion_tab = Interface()
        tab_widget.addTab(conversion_tab, "Convert Images to Video")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss = "css/style.qss"
    with open(qss, "r") as fh:
        app.setStyleSheet(fh.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
