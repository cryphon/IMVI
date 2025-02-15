from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):

    def __init__(self, text, style="InfoButton", action=None, parent=None):
        super().__init__(text, parent)
        if action is not None and callable(action):
            self.clicked.connect(action)
        self.setObjectName(style)
