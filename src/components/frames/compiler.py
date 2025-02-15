import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSlider, QTabWidget,
                             QVBoxLayout, QWidget)

from components.layout import Header
from components.tabs import GifTab, VideoTab


class Compiler(QMainWindow):

    def __init__(self, parent=None):
        super(Compiler, self).__init__()
        self.image_paths = parent.image_paths
        self.setMinimumSize(300, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create a container widget to hold both header and content
        self.container = QWidget()
        self.setCentralWidget(self.container)

        # Create a vertical layout for the container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = Header(self, title="Compiler")
        self.layout.addWidget(self.header)

        # Create and add the tab widget
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        video_tab = VideoTab(self)
        gif_tab = GifTab(self)
        self.tab_widget.addTab(video_tab, "to MP4")
        self.tab_widget.addTab(gif_tab, "to GIF")
