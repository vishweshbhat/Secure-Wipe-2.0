from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from src.wipe_history import load_wipe_history

class VerifyPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Verify Secure Wipe")

        layout = QVBoxLayout(self)

        label = QLabel("Paste or enter SHA256 hash/code to verify deletion:")
        layout.addWidget(label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Paste hash here")
        layout.addWidget(self.input)

        self.verify_btn = QPushButton("Verify")
        self.verify_btn.clicked.connect(self.verify_hash)
        layout.addWidget(self.verify_btn)

    def set_verification_hash(self, hash_value: str):
        self.input.setText(hash_value)

    def verify_hash(self):
        input_hash = self.input.text().strip()
        if not input_hash:
            QMessageBox.warning(self, "Input Required", "Please enter a hash to verify.")
            return

        history = load_wipe_history()
        for record in history:
            if record.get("file_hash") == input_hash:
                QMessageBox.information(
                    self,
                    "Verification Success",
                    (f"Hash verified successfully!\n\n"
                     f"File: {record.get('file_name')}\n"
                     f"Deleted At (UTC): {record.get('deleted_at')}")
                )
                return

        QMessageBox.warning(self, "Verification Failed", "Hash not found in wipe history.")
