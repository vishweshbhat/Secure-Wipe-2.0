from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.label = QLabel("Settings Page (Coming Soon)")
        self.label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label)
