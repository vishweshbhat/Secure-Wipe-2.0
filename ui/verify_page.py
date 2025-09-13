from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
import datetime
import pytz

from src.wipe_history import load_wipe_history

class VerifyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verify Secure Wipe")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        header = QLabel("🔍 Verify File Wipe Status")
        header.setStyleSheet("font-size: 30px; font-weight: bold; color: #FFD60A;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        prompt = QLabel("Paste or enter the SHA256 hash/code below:")
        prompt.setStyleSheet("font-size: 16px; color: #DDD;")
        prompt.setAlignment(Qt.AlignCenter)
        layout.addWidget(prompt)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Paste your hash here")
        self.input.setMinimumHeight(48)
        self.input.setStyleSheet("""
            QLineEdit {
                font-family: monospace; font-size: 18px; padding: 12px;
                border-radius: 10px; border: 2px solid #FFD60A;
                background-color: #181818; color: #FFD60A;
            }
            QLineEdit:focus {
                border: 2px solid #fff176;
                background-color: #1e1e1e;
            }
        """)
        layout.addWidget(self.input)

        self.verify_btn = QPushButton("Verify ✅")
        self.verify_btn.setFixedHeight(44)
        self.verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD60A; color: black; font-weight: bold; font-size: 18px;
                border-radius: 12px; padding: 12px 0;
            }
            QPushButton:hover {
                background-color: #ffe066;
            }
        """)
        self.verify_btn.clicked.connect(self.verify_hash)
        layout.addWidget(self.verify_btn)

        self.result_frame = QFrame()
        self.result_frame.setStyleSheet("""
            QFrame {
                background-color: #292929;
                border-radius: 16px;
                padding: 20px;
                margin-top: 24px;
            }
        """)
        self.result_layout = QVBoxLayout(self.result_frame)
        self.result_layout.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 20px;")
        self.result_layout.addWidget(self.result_label)

        layout.addWidget(self.result_frame)

    def set_verification_hash(self, hash_value: str):
        self.input.setText(hash_value)

    def verify_hash(self):
        input_hash = self.input.text().strip().lower()
        if not input_hash:
            QMessageBox.warning(self, "Input Required", "Please enter a hash to verify.")
            return

        history = load_wipe_history()
        for record in history:
            record_hash = record.get("file_hash", "").strip().lower()
            if record_hash == input_hash:
                try:
                    utc_dt = datetime.datetime.fromisoformat(record.get("deleted_at").replace("Z", "+00:00"))
                    ist_tz = pytz.timezone("Asia/Kolkata")
                    ist_dt = utc_dt.astimezone(ist_tz)
                    ist_str = ist_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
                except Exception:
                    ist_str = record.get("deleted_at")

                self.show_message(f"✅ Hash Verified!\nFile: {record.get('file_name')}\nDeleted At (IST): {ist_str}", error=False)
                return

        self.show_message("❌ Verification Failed! Hash not found in wipe history.", error=True)

    def show_message(self, message, error=False):
        color = "#FF5252" if error else "#00C853"
        self.result_label.setText(message)
        self.result_label.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: bold;")
