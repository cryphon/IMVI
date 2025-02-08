import os
import sys

import cv2
from list_widget import ListWidget
from PyQt5.QtCore import QMimeData, QRect, Qt
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPalette
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QPushButton,
                             QSlider, QVBoxLayout, QWidget)


class VideoCompiler(QWidget):

    def __init__(self, parent=None):
        super(VideoCompiler, self).__init__(parent)
        self.image_paths = []  # List to store image file paths
        self.setAcceptDrops(True)
        self._create_ui()

    def _create_ui(self):
        main_layout = QVBoxLayout(self)

        # List widget to show added images
        self.list_widget = ListWidget(self)
        main_layout.addWidget(self.list_widget)

        # Button row for adding, removing, and reordering images
        btn_layout = QHBoxLayout()
        self.remove_btn = QPushButton("Remove Selected")
        self.up_btn = QPushButton("Move Up")
        self.down_btn = QPushButton("Move Down")
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)
        main_layout.addLayout(btn_layout)

        # Connect button signals
        self.remove_btn.clicked.connect(self.remove_selected)
        self.up_btn.clicked.connect(self.move_up)
        self.down_btn.clicked.connect(self.move_down)

        # FPS control
        fps_layout = QHBoxLayout()
        fps_label = QLabel("FPS:")
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(0)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(30)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)

        self.fps_value = QLabel("30")
        self.fps_slider.valueChanged.connect(
            lambda v: self.fps_value.setText(str(v)))

        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(self.fps_slider)
        fps_layout.addWidget(self.fps_value)
        main_layout.addLayout(fps_layout)

        # Compile video button
        self.compile_btn = QPushButton("Compile Video")
        main_layout.addWidget(self.compile_btn)
        self.compile_btn.clicked.connect(self.compile_video)

        # Status label to display messages
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def add_images(self):
        """Open a file dialog to select multiple images and add them to the list."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if paths:
            self.image_paths.extend(paths)
            self.update_list_widget()

    def update_list_widget(self):
        """Refresh the list widget to show the current image file names."""
        self.list_widget.clear()
        for path in self.image_paths:
            self.list_widget.addItem(os.path.basename(path))

    def remove_selected(self):
        """Remove selected items from the list."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        # Remove items starting from the bottom so that indices stay valid.
        for item in sorted(self.list_widget.selectedItems(),
                           key=lambda x: self.list_widget.row(x),
                           reverse=True):
            index = self.list_widget.row(item)
            self.image_paths.pop(index)
        self.update_list_widget()
        self.list_widget.setCurrentRow(index - 1)

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

    def compile_video(self):
        """Compile the selected images into a video file using OpenCV."""
        if not self.image_paths:
            self.status_label.setText("No images selected!")
            return

        fps = self.fps_slider.value()

        # Ask user for output file location
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Video", "", "MP4 Files (*.mp4);;All Files (*)")
        if not output_path:
            return

        try:
            # Read the first image to determine frame size
            first_image = cv2.imread(self.image_paths[0])
            if first_image is None:
                self.status_label.setText("Error reading the first image!")
                return
            height, width = first_image.shape[:2]

            # Initialize the video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            total_images = len(self.image_paths)
            for i, path in enumerate(self.image_paths):
                self.status_label.setText(
                    f"Processing image {i+1}/{total_images}...")
                QApplication.processEvents()  # Keep UI responsive
                frame = cv2.imread(path)
                if frame is None:
                    self.status_label.setText(f"Error reading image: {path}")
                    continue
                # Resize frame if dimensions differ
                if frame.shape[:2] != (height, width):
                    frame = cv2.resize(frame, (width, height))
                out.write(frame)

            out.release()
            self.status_label.setText(
                "Video compilation completed successfully!")
        except Exception as e:
            self.status_label.setText(f"Error during compilation: {str(e)}")

    def dragEnterEvent(self, event):
        """Accept drag events that contain URLs (file paths)."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop events by adding the dropped files to the list."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.image_paths.append(file_path)
        self.update_list_widget()
