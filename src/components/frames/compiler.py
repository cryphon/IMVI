from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMessageBox

from components.layout import Header
from components.tabs import GifTab, VideoTab  # adjust import path if needed


class Compiler(QMainWindow):
    # Emitted when a compilation (video or GIF) completes successfully
    compilationFinished = pyqtSignal()

    def __init__(self, parent=None, image_paths=None):
        super(Compiler, self).__init__(parent)
        # Only the selected images are passed in from VideoInterface
        self.image_paths = list(image_paths or [])

        self.setMinimumSize(300, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Root container
        self.container = QWidget()
        self.setCentralWidget(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = Header(self, title="Compiler")
        layout.addWidget(self.header)

        # Tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # to MP4 tab (VideoTab reads self.image_paths from its parent = Compiler)
        self.video_tab = VideoTab(self)
        self.tab_widget.addTab(self.video_tab, "to MP4")
        if hasattr(self.video_tab, "compileVideoSuccessful"):
            self.video_tab.compileVideoSuccessful.connect(self._handle_compiled)

        self.gif_tab = GifTab(self)
        self.tab_widget.addTab(self.gif_tab, "to GIF")
        if hasattr(self.gif_tab, "compileGIFSuccessful"):
            self.gif_tab.compileGIFSuccessful.connect(self._handle_compiled)

    def _handle_compiled(self):
        """Notify, emit, and close after a successful compile."""
        QMessageBox.information(self, "Compilation", "Compiled successfully!")
        self.compilationFinished.emit()
        self.close()