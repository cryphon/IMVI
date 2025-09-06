from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..core import Button
from ..layout import ThumbnailViewer
from .compiler import Compiler


class VideoInterface(QWidget):
    def __init__(self, parent=None):
        super(VideoInterface, self).__init__(parent)
        self.image_paths = []  # shared with ThumbnailViewer
        self._create_ui()

    def _create_ui(self):
        main_layout = QVBoxLayout(self)

        # Thumbnail grid (handles dialog + drag & drop itself)
        self.list_widget = ThumbnailViewer(self)
        self.list_widget.selectionChanged.connect(
            lambda n: self.compile_btn.setEnabled(n > 0)
        )
        main_layout.addWidget(self.list_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        self.compile_btn = Button("Compile Video", style="ActionButton", action=self.openCompiler)
        self.compile_btn.setEnabled(False)  # enabled when selection > 0
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.compile_btn)

    def update_list_widget(self):
        """Refresh the thumbnail grid."""
        self.list_widget.update_grid()

    def clear_image_list(self):
        """Clear all images/selection after successful compile."""
        self.list_widget.clear_all()

    def openCompiler(self):
        """Open the Compiler window with ONLY the selected images."""
        selected = self.list_widget.selected_image_paths()
        if not selected:
            return  # or show a QMessageBox warning

        self.compiler_window = Compiler(self, image_paths=selected)
        self.compiler_window.compilationFinished.connect(self.clear_image_list)
        self.compiler_window.show()
