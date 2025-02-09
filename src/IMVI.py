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

        self.setStyleSheet("""
            QMainWindow { 
    background-color: #1e1e1e; 
}
QLabel { 
    color: #e0e0e0; 
    font-size: 14px; 
}
QPushButton {
    background-color: #2d5e7e;
    color: #ffffff;
    padding: 6px;
    border: none;
    border-radius: 4px;
}
QPushButton:hover { 
    background-color: #3d7eae; 
}
QTabWidget::pane {
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 20px;
}
QTabBar::tab {
    background: #2d2d2d;
    padding: 10px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background: #3d3d3d;
    color: #ffffff;
    border-bottom: 2px solid #2d5e7e;
}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
