from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget


class CustomHeader(QFrame):

    def __init__(self, parent, title="IMVI"):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setObjectName("Header")
        self.setAutoFillBackground(True)

        # Ensure it stretches across the full width of the parent window
        self.setGeometry(0, 0, parent.width(), 40)
        parent.installEventFilter(self)  # Capture resize events

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Title Label
        self.title = QLabel(title, self)
        self.title.setObjectName(
            "HeaderTitle")  # Object name for QSS targeting

        # Close Button
        self.close_button = QPushButton("✖", self)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet(
            "background: transparent; color: white; border: none; font-size: 16px;"
        )
        self.close_button.clicked.connect(self.parent.close)

        # Add widgets to layout
        layout.addWidget(self.title)
        layout.addStretch()  # Pushes the button to the right
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.dragging = False  # Flag for dragging
        self.offset = QPoint()

    def mousePressEvent(self, event):
        """Start dragging when clicking the header (except on the button)."""
        if event.button() == Qt.LeftButton and event.pos().x(
        ) < self.width() - 40:  # Exclude close button area
            self.dragging = True
            self.offset = event.globalPos() - self.parent.frameGeometry(
            ).topLeft()

    def mouseMoveEvent(self, event):
        """Move the window while dragging."""
        if self.dragging:
            self.parent.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        """Stop dragging when releasing the mouse."""
        self.dragging = False

    def eventFilter(self, obj, event):
        """Adjust header width when the main window resizes."""
        if obj == self.parent and event.type() == event.Resize:
            self.setGeometry(0, 0, self.parent.width(), 40)
        return super().eventFilter(obj, event)
