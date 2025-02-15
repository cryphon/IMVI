from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget

from components.core import ImageListItem


class ListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

    def mousePressEvent(self, event):
        """Open file dialog on click of list widget"""
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

    def update_list_widget(self):
        """Update the list widget with the current image paths."""
        self.clear()
        for path in self.parent_widget.image_paths:
            item = QListWidgetItem()
            item_widget = ImageListItem(path, self)
            item.setSizeHint(item_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, item_widget)
