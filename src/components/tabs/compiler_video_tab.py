import cv2
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QHBoxLayout,
                             QLabel, QPushButton, QSlider, QVBoxLayout,
                             QWidget)


class VideoTab(QWidget):

    # define signal
    compileVideoSuccessful = pyqtSignal()

    def __init__(self, parent=None):
        super(VideoTab, self).__init__()
        self.image_paths = parent.image_paths
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout(self)

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

        res_layout = QHBoxLayout()
        res_label = QLabel("Resolution Scaling:")
        self.res_dropdown = QComboBox()
        self.res_dropdown.addItems(["Original", "720p", "1080p"])
        self.res_dropdown.setStyleSheet("""
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
        res_layout.addWidget(res_label)
        res_layout.addWidget(self.res_dropdown)
        main_layout.addLayout(res_layout)

        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality (0-100):")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(50)
        self.quality_slider.setTickInterval(1)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)

        self.quality_value = QLabel("30")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_value.setText(str(v)))

        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)
        main_layout.addLayout(quality_layout)

        btn_layout = QHBoxLayout()
        self.compile_btn = QPushButton("Compile")
        btn_layout.addWidget(self.compile_btn)
        main_layout.addLayout(btn_layout)

        self.compile_btn.clicked.connect(self.compile_video)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def compile_video(self):
        if not self.image_paths:
            self.status_label.setText("No images selected!")
            return

        print(self.image_paths)

        fps = self.fps_slider.value()

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Video", "", "MP4 Files (*.mp4);;All Files (*)")
        if not output_path:
            return

        try:
            # Read first image to get frame size
            first_image = cv2.imread(self.image_paths[0])
            if first_image is None:
                self.status_label.setText("Error reading the first image!")
                return

            height, width = first_image.shape[:2]
            target_size = (width, height)  # default

            if self.res_dropdown.currentText() == "720p":
                target_size = (1280, 720)
            elif self.res_dropdown.currentText() == "1080p":
                target_size = (1920, 1080)

            # init video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path,
                                  fourcc,
                                  fps,
                                  target_size,
                                  params=[
                                      cv2.VIDEOWRITER_PROP_QUALITY,
                                      self.quality_slider.value()
                                  ])

            total_images = len(self.image_paths)
            for i, path in enumerate(self.image_paths):
                self.status_label.setText(
                    f"Processing image {i+1}/{total_images}...")
                QApplication.processEvents()
                frame = cv2.imread(path)
                if frame is None:
                    self.status_label.setText(f"Error reading image: {path}")
                    continue

                frame = cv2.resize(frame, target_size)
                out.write(frame)

            out.release()
            self.status_label.setText(
                "Video compilation completed successfully!")

            self.compileVideoSuccessful.emit()

        except Exception as e:
            self.status_label.setText(f"Error during compilation: {str(e)}")
            print(f"Error during compilation: {str(e)}")
