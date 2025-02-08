from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPalette
from PyQt5.QtWidgets import QFileDialog, QListWidget
# from video_compiler import VideoCompiler


class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent  # Store the parent widget reference

        # Set gray background
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(33, 33, 33))  # Light gray
        self.setPalette(palette)

        self.setStyleSheet("color: #e0e0e0;")  # Light gray text

    def mousePressEvent(self, event):
        # Check if the list is empty and left mouse button is clicked
        if self.count() == 0 and event.button() == Qt.LeftButton:
            self.openFileDialog()
        else:
            super().mousePressEvent(event)

    def openFileDialog(self):
        """Open a file dialog to select multiple images and add them to the list."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if paths:
            self.parent_widget.image_paths.extend(paths)
            self.parent_widget.update_list_widget()
