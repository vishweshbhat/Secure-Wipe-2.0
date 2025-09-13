from PySide6.QtWidgets import QToolBar, QPushButton
from PySide6.QtCore import Signal

class NavigationBar(QToolBar):
    home_clicked = Signal()
    verify_clicked = Signal()
    settings_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setMovable(False)
        self.setFloatable(False)

        self.home_btn = QPushButton("Home")
        self.verify_btn = QPushButton("Verify")
        self.settings_btn = QPushButton("Settings")

        self.addWidget(self.home_btn)
        self.addWidget(self.verify_btn)
        self.addWidget(self.settings_btn)

        self.home_btn.clicked.connect(self.home_clicked)
        self.verify_btn.clicked.connect(self.verify_clicked)
        self.settings_btn.clicked.connect(self.settings_clicked)
