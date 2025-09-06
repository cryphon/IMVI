import glob
import os
from datetime import datetime

import cv2
from PIL import Image
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSlider, QVBoxLayout,
                             QWidget)


class GifTab(QWidget):

    # define signal
    compileGIFSuccessful = pyqtSignal()

    def __init__(self, parent=None):
        super(GifTab, self).__init__()
        self.parent = parent
        self.create_ui()

    def create_ui(self):
        """Create UI for GIF tab"""
        main_layout = QVBoxLayout(self)

        # FPS control
        fps_layout = QHBoxLayout()
        fps_label = QLabel("SLOW")
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(61)
        self.fps_slider.setValue(30)
        self.fps_slider.setTickInterval(5)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_value = QLabel("FAST")
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(self.fps_slider)
        fps_layout.addWidget(self.fps_value)
        main_layout.addLayout(fps_layout)

        btn_layout = QHBoxLayout()
        self.compile_btn = QPushButton("Compile GIF")
        btn_layout.addWidget(self.compile_btn)
        main_layout.addLayout(btn_layout)
        self.compile_btn.clicked.connect(self.compile_gif)

        # Status label
        self.status_label = QLabel("Click Compile GIF to start")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def compile_gif(self):
        """Handle GIF compilation using parent's image paths"""
        if not self.parent or not self.parent.image_paths:
            self.status_label.setText("No images selected!")
            return

        images = []

        for filename in self.parent.image_paths:
            im = Image.open(filename)
            h, w = im.size
            images.append(im)

        if not images:
            self.status_label.setText("No images found in selected paths!")
            return

        fps = abs(self.fps_slider.value() - 60)

        n_imgs = len(self.parent.image_paths)
        duration = self.calculate_duration(n_imgs, fps=fps)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"compiled_gif_{fps}FPS_{timestamp}.gif"

        # Get save location from first image dir
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save GIF",
            os.path.join(os.path.dirname(self.parent.image_paths[0]),
                         default_name), "GIF Files (*.gif);;All Files (*)")

        if not output_path:  # User cancelled
            return

        # Save the GIF
        images[0].save(output_path,
                       save_all=True,
                       append_images=images[1:],
                       optimize=False,
                       duration=duration,
                       loop=0)

        self.status_label.setText(
            f"GIF compilation completed successfully!\nSaved as: {output_path}"
        )

        self.compileGIFSuccessful.emit()

    def calculate_duration(self, num_images, fps=30):

        # Calculate duration in seconds
        duration_seconds = num_images / fps

        # Convert to hours, minutes, seconds
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)

        return duration_seconds
