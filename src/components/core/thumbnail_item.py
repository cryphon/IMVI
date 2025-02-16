import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class ThumbnailItem(QWidget):

    def __init__(self, path, parent=None):
        super().__init__(parent)

        # Image thumbnail
        pixmap = QPixmap(path).scaled(80, 80, Qt.KeepAspectRatio,
                                      Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Text label
        text = Path(os.path.basename(path)).stem[:20]
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)

        # Apply layout to self
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(text_label)
        layout.setSpacing(2)
        self.setLayout(
            layout
        )  # <- This ensures the widget actually gets rendered properly.
