from PyQt5.QtWidgets import QLabel


class Label(QLabel):

    def __init__(self, text, style="InfoLabel", action=None, parent=None):
        super().__init__(text, parent)
        if action is not None and callable(action):
            self.clicked.connect(action)
        self.setObjectName(style)
