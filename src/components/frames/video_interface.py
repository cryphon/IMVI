import os
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
                             QListWidgetItem, QVBoxLayout, QWidget)

from ..core import Button, ImageListItem
from ..layout import ListWidget, ThumbnailViewer

from .compiler import Compiler


class VideoInterface(QWidget):

    def __init__(self, parent=None):
        super(VideoInterface, self).__init__(parent)
        self.image_paths = []
        self.setAcceptDrops(True)
        self._create_ui()

    def _create_ui(self):
        """Create UI for the application"""
        main_layout = QVBoxLayout(self)

        # List widget
        self.list_widget = ThumbnailViewer(self)
        main_layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_images_btn = Button("Add images",
                                     style="InfoButton",
                                     action=self.add_images)
        self.up_btn = Button("Move Up",
                             style="InfoButton",
                             action=self.move_up)
        self.down_btn = Button("Move Down",
                               style="InfoButton",
                               action=self.move_down)
        self.compile_btn = Button("Compile Video",
                                  style="ActionButton",
                                  action=self.openCompiler)
        btn_layout.addWidget(self.add_images_btn)
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)
        main_layout.addLayout(btn_layout)

        main_layout.addWidget(self.compile_btn)

    def add_images(self):
        """Open a file dialog to select multiple images and add them to the list."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if paths:
            self.image_paths.extend(paths)
            self.update_list_widget()

    def update_list_widget(self):
        """Refresh the list widget to show the current image file names with controls."""
        for child in self.list_widget.findChildren(QWidget):
            child.deleteLater()  # Delete each widget properly

        for path in self.image_paths:
            item = QListWidgetItem()
            item_widget = ImageListItem(path, self.list_widget)
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

    def clear_image_list(self):
        self.image_paths = []
        self.update_list_widget()

    def move_up(self):
        """Move the selected image up in the list."""
        current_row = self.list_widget.currentRow()
        if current_row <= 0:
            return
        self.image_paths[current_row], self.image_paths[current_row - 1] = (
            self.image_paths[current_row - 1], self.image_paths[current_row])
        self.update_list_widget()
        self.list_widget.setCurrentRow(current_row - 1)

    def move_down(self):
        """Move the selected image down in the list."""
        current_row = self.list_widget.currentRow()
        if current_row < 0 or current_row >= len(self.image_paths) - 1:
            return
        self.image_paths[current_row], self.image_paths[current_row + 1] = (
            self.image_paths[current_row + 1], self.image_paths[current_row])
        self.update_list_widget()
        self.list_widget.setCurrentRow(current_row + 1)

    def dragEnterEvent(self, event):
        """Accept drag events that contain URLs (file paths)."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop events by adding the dropped files to the list in sorted order."""
        new_files = []

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()

            if os.path.isdir(file_path):
                for root, _, files in os.walk(file_path):
                    for file in files:
                        if file.lower().endswith(
                            ('.png', '.jpg', '.jpeg', '.bmp')):
                            new_files.append(os.path.join(root, file))
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                new_files.append(file_path)

        # Sort new files before adding them
        new_files.sort(key=lambda x: os.path.basename(x))

        # Ensure first batch is always in correct order
        if not self.image_paths:
            self.image_paths = new_files
        else:
            self.image_paths.extend(new_files)

        self.update_list_widget()

    def openCompiler(self):
        if self.image_paths:
            self.compiler_window = Compiler(self)
            self.compiler_window.compilationFinished.connect(self.clear_image_list)
            self.compiler_window.show()
