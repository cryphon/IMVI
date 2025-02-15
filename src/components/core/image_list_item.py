from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QPushButton, QWidget)


class ImageListItem(QWidget):

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        # File name label
        self.label = QLabel(image_path.split('/')[-1])  # Show only filename
        self.label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(self.label)
        layout.addStretch()

        # Control buttons
        self.delete_btn = QPushButton("✖")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #e0e0e0;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)

        layout.addWidget(self.delete_btn)
        self.setLayout(layout)

        # Store the full path
        self.image_path = image_path

        # Connect delete button
        self.delete_btn.clicked.connect(self.delete_item)

    def delete_item(self):
        list_widget = self.parent().parent()
        if isinstance(list_widget,
                      QListWidget):  # Check for QListWidget instead
            # Remove from parent's image_paths list
            if hasattr(list_widget.parent_widget, 'image_paths'):
                if self.image_path in list_widget.parent_widget.image_paths:
                    list_widget.parent_widget.image_paths.remove(
                        self.image_path)

            # Remove from list widget
            for i in range(list_widget.count()):
                if list_widget.itemWidget(list_widget.item(i)) is self:
                    list_widget.takeItem(i)
                    break


# Add this method to your ListWidget class:
def update_list_widget(self):
    """Update the list widget with the current image paths."""
    self.clear()
    for path in self.parent_widget.image_paths:
        item = QListWidgetItem()
        item_widget = ImageListItem(path, self)
        item.setSizeHint(item_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, item_widget)
