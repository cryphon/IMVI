import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout, QLabel,
                             QListWidget, QListWidgetItem, QMainWindow,
                             QPushButton, QScrollArea, QVBoxLayout, QWidget)

from components.core import ThumbnailItem


class ThumbnailViewer(QWidget):
    """A scrollable widget that displays images in a grid layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Main layout
        self.layout = QVBoxLayout(self)
        self.setFixedSize(600, 400)
        # Scroll area setup
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Container for grid
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(5)  # Space between thumbnails
        self.scroll_area.setWidget(self.container)

        # Add widgets to layout
        self.layout.addWidget(self.scroll_area)

    def mousePressEvent(self, event):
        """Open file dialog on click of list widget"""
        if len(self.parent.image_paths) == 0 and event.button(
        ) == Qt.LeftButton:
            self.openFileDialog()
        else:
            super().mousePressEvent(event)

    def openFileDialog(self):
        """Opens file dialog to select images and adds them to the grid."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if paths:
            self.parent.image_paths.extend(paths)
            self.update_grid()

    def update_grid(self):
        """Updates the grid layout with new thumbnails."""
        # Remove existing items
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # Add new items
        cols = 3  # Number of columns
        for index, path in enumerate(self.parent.image_paths):
            row, col = divmod(index, cols)

            thumb_widget = ThumbnailItem(path)
            # Add widget to grid
            self.grid_layout.addWidget(thumb_widget, row, col)

        self.container.setLayout(self.grid_layout)
