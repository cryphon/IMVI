import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSlider, QTabWidget,
                             QVBoxLayout, QWidget)

from gif_tab import GifTab
from video_tab import VideoTab


class Compiler(QMainWindow):

    def __init__(self, parent=None):
        super(Compiler, self).__init__()
        self.setWindowTitle("Compiler")
        self.image_paths = parent.image_paths
        self.setMinimumSize(300, 300)
        self.create_ui()

    def create_ui(self):
        """Create UI for compiler window"""
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        video_tab = VideoTab(self)
        gif_tab = GifTab(self)
        tab_widget.addTab(video_tab, "to MP4")
        tab_widget.addTab(gif_tab, "to GIF")
