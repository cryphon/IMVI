import os
import re
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import (
    QFileDialog, QGridLayout, QScrollArea, QVBoxLayout, QWidget,
    QPushButton, QHBoxLayout
)

from components.core import ThumbnailItem


class ThumbnailViewer(QWidget):
    """Scrollable thumbnail grid with drag & drop + selection."""
    IMAGE_EXTS = {'.png', '.jpg', '.jpeg'}

    # Notify parent layers
    imagesUpdated = pyqtSignal()
    selectionChanged = pyqtSignal(int)  # emits selected count

    def _natural_key(self, p: str):
        name = os.path.basename(p)
        return [int(t) if t.isdigit() else t.lower() for t in re.findall(r'\d+|\D+', name)]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)

        # Selection state (store image paths)
        self._selected = set()

        # Map widget -> path for quick hit-tests
        self._widget_to_path = {}

        # Layout
        self.layout = QVBoxLayout(self)
        self.setFixedSize(600, 400)

        # ---- Controls row (Clear button) ----
        controls = QHBoxLayout()
        controls.setContentsMargins(0, 0, 0, 0)
        controls.setSpacing(6)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setToolTip("Clear all images")
        self.clear_btn.clicked.connect(self.clear_all)
        controls.addStretch(1)
        controls.addWidget(self.clear_btn)

        self.layout.addLayout(controls)
        # ------------------------------------

        # Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Container with grid
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(5)
        self.container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.container)

        self.layout.addWidget(self.scroll_area)

        # Styles
        self._normal_css = "QWidget { border: 1px solid #444; border-radius: 6px; }"
        self._selected_css = "QWidget { border: 2px solid #3b82f6; border-radius: 6px; }"

        # If parent already has images, select them all initially
        if getattr(self.parent, "image_paths", None):
            self._selected = set(self.parent.image_paths)
            self.update_grid()
            self.selectionChanged.emit(len(self._selected))

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
                # sort dirs and files for stable traversal
                for root, dirs, files in os.walk(str(path)):
                    dirs.sort(key=str.lower)  # ensure predictable dir order
                    # natural sort files within each directory
                    files.sort(key=lambda f: self._natural_key(f))
                    for f in files:
                        if Path(f).suffix.lower() in self.IMAGE_EXTS:
                            new_files.append(os.path.join(root, f))
            elif path.suffix.lower() in self.IMAGE_EXTS:
                new_files.append(str(path))

        if new_files:
            # natural sort the whole dropped batch once
            new_files.sort(key=self._natural_key)
            self._add_paths(new_files)
            event.acceptProposedAction()
        else:
            event.ignore()

    def _add_paths(self, paths):
        """Append in given order, skip dupes, auto-select newly added."""
        added_any = False
        for p in paths:
            if p not in self.parent.image_paths:
                self.parent.image_paths.append(p)
                self._selected.add(p)   # auto-select new item
                added_any = True

        if added_any:
            self._selected.intersection_update(self.parent.image_paths)
            self.update_grid()
            self.imagesUpdated.emit()
            self.selectionChanged.emit(len(self._selected))

    def update_grid(self):
        # Clear mapping and widgets
        self._widget_to_path.clear()
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.removeEventFilter(self)
                w.deleteLater()

        # Rebuild thumbnails in the exact order of parent.image_paths
        cols = 3
        for index, path in enumerate(self.parent.image_paths):
            row, col = divmod(index, cols)
            thumb_widget = ThumbnailItem(path)
            thumb_widget.setStyleSheet(
                self._selected_css if path in self._selected else self._normal_css
            )
            thumb_widget.installEventFilter(self)  # intercept clicks
            self.grid_layout.addWidget(thumb_widget, row, col)
            self._widget_to_path[thumb_widget] = path

        self.container.setLayout(self.grid_layout)

    # Intercept clicks on child thumbnails to toggle selection
    def eventFilter(self, obj, event):
        if obj in self._widget_to_path and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            path = self._widget_to_path[obj]
            if path in self._selected:
                self._selected.remove(path)
                obj.setStyleSheet(self._normal_css)
            else:
                self._selected.add(path)
                obj.setStyleSheet(self._selected_css)

            self._selected.intersection_update(self.parent.image_paths)
            self.selectionChanged.emit(len(self._selected))
            return True  # consume the click
        return super().eventFilter(obj, event)

    def selected_image_paths(self):
        """Return selected images in original order."""
        if not self._selected:
            return []
        return [p for p in self.parent.image_paths if p in self._selected]

    def clear_selection(self):
        if not self._selected:
            return
        self._selected.clear()
        self.update_grid()
        self.selectionChanged.emit(0)

    def select_all(self):
        self._selected = set(self.parent.image_paths)
        self.update_grid()
        self.selectionChanged.emit(len(self._selected))

    def remove_selected(self):
        """Remove selected items from the list and UI (order of remaining preserved)."""
        if not self._selected:
            return
        self.parent.image_paths = [p for p in self.parent.image_paths if p not in self._selected]
        self._selected.clear()
        self.update_grid()
        self.selectionChanged.emit(0)
        self.imagesUpdated.emit()

    def clear_all(self):
        """Clear all images and selection."""
        if not self.parent.image_paths and not self._selected:
            return
        self.parent.image_paths.clear()
        self._selected.clear()
        self.update_grid()
        self.selectionChanged.emit(0)
        self.imagesUpdated.emit()
