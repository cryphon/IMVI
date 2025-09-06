import os
import sys
from typing import List

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImageReader, QImageWriter
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QFileDialog,
                             QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QMessageBox, QProgressDialog,
                             QPushButton, QSlider, QVBoxLayout, QWidget)

LOSSY_FORMATS = {"jpg", "jpeg", "webp"}


def normalized_format(fmt: str) -> str:
    f = fmt.lower().strip().lstrip(".")
    return {"jpeg": "jpg"}.get(f, f)


def unique_path(directory: str, base_name: str, ext: str) -> str:
    path = os.path.join(directory, f"{base_name}.{ext}")
    if not os.path.exists(path):
        return path
    n = 1
    while True:
        candidate = os.path.join(directory, f"{base_name} ({n}).{ext}")
        if not os.path.exists(candidate):
            return candidate
        n += 1


class ImageInterface(QWidget):

    def __init__(self, parent=None):
        super(ImageInterface, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setAcceptDrops(True)
        # Files list
        self.fileList = QListWidget()
        self.fileList.setSelectionMode(QListWidget.ExtendedSelection)
        self.fileList.setStyleSheet("QListWidget, { color: white;}")

        # Buttons
        self.addBtn = QPushButton("Add…")
        self.removeBtn = QPushButton("Remove")
        self.clearBtn = QPushButton("Clear")
        self.convertBtn = QPushButton("Convert")

        # Format & quality
        self.formatBox = QComboBox()
        fmts = sorted({
            bytes(fmt).decode("utf-8").lower()
            for fmt in QImageWriter.supportedImageFormats()
        })
        preferred = ["png", "jpg", "webp", "bmp", "tiff"]
        ordered = preferred + [f for f in fmts if f not in preferred]
        seen = set()
        for f in ordered:
            f = normalized_format(f)
            if f and f not in seen:
                self.formatBox.addItem(f.upper(), f)
                seen.add(f)

        self.qualityLbl = QLabel("Quality: 90")
        self.qualitySlider = QSlider(Qt.Horizontal)
        self.qualitySlider.setRange(1, 100)
        self.qualitySlider.setValue(90)

        # Output dir
        self.outDirEdit = QLineEdit()
        self.outDirEdit.setPlaceholderText(
            "Output folder (defaults to each file's folder)")
        self.outDirEdit.setStyleSheet("""
            QLineEdit {
                color: white;
                background-color: #2b2b2b;
                selection-background-color: #3a3a3a;
                selection-color: white;
            }
        """)
        self.browseBtn = QPushButton("Browse…")

        # Layouts
        leftBtns = QHBoxLayout()
        leftBtns.addWidget(self.addBtn)
        leftBtns.addWidget(self.removeBtn)
        leftBtns.addWidget(self.clearBtn)

        fmtRow = QHBoxLayout()
        fmtRow.addWidget(QLabel("Output format:"))
        fmtRow.addWidget(self.formatBox, 1)
        self.formatBox.setStyleSheet("""
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

        fmtRow.addSpacing(10)
        fmtRow.addWidget(self.qualityLbl)
        fmtRow.addWidget(self.qualitySlider)

        outRow = QHBoxLayout()
        outRow.addWidget(QLabel("Output folder:"))
        outRow.addWidget(self.outDirEdit, 1)
        outRow.addWidget(self.browseBtn)

        root = QVBoxLayout(self)
        root.addWidget(self.fileList, 1)
        root.addLayout(leftBtns)
        root.addSpacing(6)
        root.addLayout(fmtRow)
        root.addLayout(outRow)
        root.addWidget(self.convertBtn)

        # Shortcuts
        removeAct = QAction(self)
        removeAct.setShortcut("Delete")
        removeAct.triggered.connect(self.onRemoveSelected)
        self.addAction(removeAct)

        # Signals
        self.addBtn.clicked.connect(self.onAddFiles)
        self.removeBtn.clicked.connect(self.onRemoveSelected)
        self.clearBtn.clicked.connect(self.fileList.clear)
        self.browseBtn.clicked.connect(self.onBrowseOutputDir)
        self.formatBox.currentIndexChanged.connect(self.onFormatChanged)
        self.qualitySlider.valueChanged.connect(
            lambda v: self.qualityLbl.setText(f"Quality: {v}"))
        self.convertBtn.clicked.connect(self.onConvert)

        self.onFormatChanged(self.formatBox.currentIndex())

    # --- Drag & drop ---
    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        urls = e.mimeData().urls()
        paths = [u.toLocalFile() for u in urls if u.isLocalFile()]
        self.addFiles(paths)

    # --- UI callbacks ---
    def onAddFiles(self):
        fmts = " ".join(f"*.{bytes(ext).decode().lower()}"
                        for ext in QImageReader.supportedImageFormats())
        files, _ = QFileDialog.getOpenFileNames(self, "Add Images", "",
                                                f"Images ({fmts})")
        if files:
            self.addFiles(files)

    def onRemoveSelected(self):
        for item in self.fileList.selectedItems():
            self.fileList.takeItem(self.fileList.row(item))

    def onBrowseOutputDir(self):
        d = QFileDialog.getExistingDirectory(self, "Choose Output Folder", "")
        if d:
            self.outDirEdit.setText(d)

    def onFormatChanged(self, _index: int):
        fmt = self.formatBox.currentData()
        lossy = fmt in LOSSY_FORMATS
        self.qualitySlider.setEnabled(lossy)
        self.qualityLbl.setEnabled(lossy)

    # --- Helpers ---
    def addFiles(self, files: List[str]):
        for f in files:
            if os.path.isfile(f):
                self.fileList.addItem(QListWidgetItem(f))

    # --- Conversion ---
    def onConvert(self):
        count = self.fileList.count()
        if count == 0:
            QMessageBox.information(self, "Nothing to do",
                                    "Add some image files first.")
            return

        out_fmt = self.formatBox.currentData()
        quality = self.qualitySlider.value()

        progress = QProgressDialog("Converting images…", "Cancel", 0, count,
                                   self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        errors = []
        for i in range(count):
            if progress.wasCanceled():
                break
            path = self.fileList.item(i).text()
            progress.setLabelText(os.path.basename(path))
            progress.setValue(i)

            reader = QImageReader(path)
            img = reader.read()
            if img.isNull():
                errors.append(f"Read failed: {path} ({reader.errorString()})")
                continue

            out_dir = self.outDirEdit.text().strip() or os.path.dirname(path)
            base = os.path.splitext(os.path.basename(path))[0]
            out_path = unique_path(out_dir, base, out_fmt)

            writer = QImageWriter(out_path, out_fmt.encode("utf-8"))
            if out_fmt in LOSSY_FORMATS:
                writer.setQuality(quality)

            if not writer.write(img):
                errors.append(
                    f"Write failed: {out_path} ({writer.errorString()})")

            QApplication.processEvents()

        progress.setValue(count)

        if errors:
            QMessageBox.warning(
                self, "Finished with errors",
                "\n".join(errors[:20]) + ("\n…" if len(errors) > 20 else ""))
        else:
            QMessageBox.information(self, "Done",
                                    "All images converted successfully!")
