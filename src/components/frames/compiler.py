import cv2
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSlider, QTabWidget,
                             QVBoxLayout, QWidget, QMessageBox)

from components.layout import Header
from components.tabs import GifTab, VideoTab


class Compiler(QMainWindow):

    # Signal that this window is completely done (used by the interface)
    compilationFinished = pyqtSignal()

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

        video_tab.compileVideoSuccessful.connect(self.handle_compiled)
        gif_tab.compileGIFSuccessful.connect(self.handle_compiled)

    def handle_compiled(self):
        self.compilationFinished.emit()
        self.close()
        QMessageBox.information(self, "Compilation", "compiled successfully!")

