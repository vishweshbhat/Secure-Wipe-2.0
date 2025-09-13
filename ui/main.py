import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QToolBar
from PySide6.QtCore import Qt

# Make sure src is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from home_page import HomePage
from verify_page import VerifyPage
from settings_page import SettingsPage
from navigation import NavigationBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Wipe Tool")
        self.setMinimumSize(500, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.home_page = HomePage()
        self.verify_page = VerifyPage()
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.home_page)      # 0
        self.stack.addWidget(self.verify_page)    # 1
        self.stack.addWidget(self.settings_page)  # 2

        self.nav_widget = NavigationBar()
        self.nav = QToolBar()
        self.nav.setMovable(False)
        self.nav.addWidget(self.nav_widget)
        self.addToolBar(Qt.BottomToolBarArea, self.nav)

        self.nav_widget.home_clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_widget.verify_clicked.connect(self.go_to_verify)
        self.nav_widget.settings_clicked.connect(lambda: self.stack.setCurrentIndex(2))

    def go_to_verify(self):
        # Pass hash from home page to verify page (if exists)
        hash_value = getattr(self.home_page, "file_hash", "")
        self.verify_page.set_verification_hash(hash_value)
        self.stack.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
