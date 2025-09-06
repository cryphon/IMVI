import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QScrollArea, QVBoxLayout, QWidget

from components.core import ThumbnailItem


class ThumbnailViewer(QWidget):
    """A scrollable widget that displays images in a grid layout with drag & drop."""
    IMAGE_EXTS = {'.png', '.jpg', '.jpeg'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)

        # Layout
        self.layout = QVBoxLayout(self)
        self.setFixedSize(600, 400)

        # Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Container with grid
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(5)
        self.scroll_area.setWidget(self.container)

        self.layout.addWidget(self.scroll_area)

    def mousePressEvent(self, event):
        if len(self.parent.image_paths) == 0 and event.button() == Qt.LeftButton:
            self.openFileDialog()
        else:
            super().mousePressEvent(event)

    def openFileDialog(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if paths:
            self._add_paths(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        new_files = []
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            if path.is_dir():
                for root, _, files in os.walk(str(path)):
                    for f in files:
                        if Path(f).suffix.lower() in self.IMAGE_EXTS:
                            new_files.append(os.path.join(root, f))
            elif path.suffix.lower() in self.IMAGE_EXTS:
                new_files.append(str(path))

        if new_files:
            self._add_paths(new_files)
            event.acceptProposedAction()
        else:
            event.ignore()

    def _add_paths(self, paths):
        # Keep order, skip duplicates
        for p in paths:
            if p not in self.parent.image_paths:
                self.parent.image_paths.append(p)
        self.update_grid()

    def update_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        cols = 3
        for index, path in enumerate(self.parent.image_paths):
            row, col = divmod(index, cols)
            thumb_widget = ThumbnailItem(path)
            self.grid_layout.addWidget(thumb_widget, row, col)

        self.container.setLayout(self.grid_layout)