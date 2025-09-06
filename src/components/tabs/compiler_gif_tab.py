import glob
import os
from datetime import datetime

import cv2
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QLabel,
                             QMessageBox, QPushButton, QSlider, QVBoxLayout,
                             QWidget)


class GifTab(QWidget):

    def __init__(self, parent=None):
        super(GifTab, self).__init__()
        self.parent = parent
        self.create_ui()

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

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

        loop_layout = QHBoxLayout()
        loop_label = QLabel("Playback:")
        self.loop_combo = QComboBox()
        self.loop_combo.addItems(["Play once", "Loop forever"])
        self.loop_combo.setStyleSheet("""
            QComboBox {
                color: white;
                background-color: #2b2b2b;
                selection-background-color: #3a3a3a;
                selection-color: white;
            }
            QComboBox QAbstractItemView {
                color: white;
                background-color: #2b2b2b;
                selection-background-color: #3a3a3a;
                selection-color: white;
            }
        """)
        loop_layout.addWidget(loop_label)
        loop_layout.addWidget(self.loop_combo)
        loop_layout.addStretch()
        main_layout.addLayout(loop_layout)

        btn_layout = QHBoxLayout()
        self.compile_btn = QPushButton("Compile GIF")
        btn_layout.addWidget(self.compile_btn)
        main_layout.addLayout(btn_layout)
        self.compile_btn.clicked.connect(self.compile_gif)

    def compile_gif(self):
        """Handle GIF compilation using parent's image paths"""
        if not self.parent or not self.parent.image_paths:
            self.show_message("Error", "No images selected!",
                              QMessageBox.Warning)
            return

        images = []

        for filename in self.parent.image_paths:
            try:
                im = Image.open(filename)
                images.append(im)
            except Exception as e:
                self.show_message("Error", f"Failed to open {filename}\n{e}",
                                  QMessageBox.Critical)
                return

        if not images:
            self.show_message("Error", "No valid images found!",
                              QMessageBox.Warning)
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
        loop_forever = (self.loop_combo.currentText() == "Loop forever")
        save_kwargs = dict(save_all=True,
                           append_images=images[1:],
                           optimize=False,
                           duration=duration)
        if loop_forever:
            save_kwargs["loop"] = 0  # 0 = infinite

        try:
            images[0].save(output_path, **save_kwargs)
            self.show_message("Success",
                              f"GIF saved successfully:\n{output_path}",
                              QMessageBox.Information)
        except Exception as e:
            self.show_message("Error", f"Failed to save GIF:\n{e}",
                              QMessageBox.Critical)

    def calculate_duration(self, num_images, fps=30):
        return max(1, int(1000 / max(1, fps)))
