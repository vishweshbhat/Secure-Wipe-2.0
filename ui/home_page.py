import os
import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit
from PySide6.QtCore import Qt
from src.wipe_engine import wipe_file, wipe_partition, wipe_os
from src.reports import generate_report
from src.wipe_history import save_wipe_record

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.file_hash = ""

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #232526, stop:1 #121212);
                color: white;
                border-radius: 18px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        header = QLabel("Secure Wipe Tool")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFD60A; margin-bottom: 24px;")
        layout.addWidget(header)

        self.status_panel = QLabel("Ready. Select a wipe action.")
        self.status_panel.setAlignment(Qt.AlignCenter)
        self.status_panel.setStyleSheet("""
            font-size: 14px; color: #bbbbbb; background: #181818;
            border-radius: 12px; padding: 12px; margin-bottom: 16px;
        """)
        layout.addWidget(self.status_panel)

        self.hash_display = QLineEdit()
        self.hash_display.setReadOnly(True)
        self.hash_display.setStyleSheet("""
            background-color: #181818; color: #FFD60A;
            border-radius: 8px; padding: 8px; font-family: monospace;
            font-size: 16px; margin-bottom: 10px;
        """)
        self.hash_display.hide()
        layout.addWidget(self.hash_display)

        file_wipe_label = QLabel("🗑️ Wipe a Specific File")
        file_wipe_label.setAlignment(Qt.AlignCenter)
        file_wipe_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 6px; color: #FFD60A;")
        layout.addWidget(file_wipe_label)

        self.select_files_btn = QPushButton("Select Files")
        self.select_files_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD60A; color: black; font-size: 16px; font-weight: bold;
                border-radius: 12px; padding: 16px 32px;
            }
            QPushButton:hover { background-color: #ffe066; color: #222; }
        """)
        self.select_files_btn.clicked.connect(self.select_and_wipe_file)
        layout.addWidget(self.select_files_btn)
        layout.addSpacing(30)

        partition_label = QLabel("💽 Wipe an Entire Partition")
        partition_label.setAlignment(Qt.AlignCenter)
        partition_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD60A; margin-bottom: 6px;")
        layout.addWidget(partition_label)

        self.select_partition_btn = QPushButton("Select Partition")
        self.select_partition_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD60A; color: black; font-size: 16px; font-weight: bold;
                border-radius: 12px; padding: 16px 32px;
            }
            QPushButton:hover { background-color: #ffe066; color: #222; }
        """)
        self.select_partition_btn.clicked.connect(self.select_and_wipe_partition)
        layout.addWidget(self.select_partition_btn)
        layout.addSpacing(30)

        os_label = QLabel("⚠️ Wipe Entire Operating System")
        os_label.setAlignment(Qt.AlignCenter)
        os_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #d32f2f; margin-bottom: 6px;")
        layout.addWidget(os_label)

        self.wipe_os_btn = QPushButton("Wipe Entire OS")
        self.wipe_os_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f; color: white; font-size: 16px; font-weight: bold;
                border-radius: 12px; padding: 16px 32px;
            }
            QPushButton:hover { background-color: #e46a6a; color: white; }
        """)
        self.wipe_os_btn.clicked.connect(self.confirm_and_wipe_os)
        layout.addWidget(self.wipe_os_btn)

    def select_and_wipe_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Wipe")
        if file_path:
            self.status_panel.setText("Computing file hash...")
            file_hash = self.compute_file_hash(file_path)
            self.hash_display.setText(file_hash)
            self.hash_display.show()
            self.file_hash = file_hash
            self.status_panel.setText("Hash ready. Wiping file...")

            success = wipe_file(file_path)
            if success:
                BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                private_key_path = os.path.join(BASE_DIR, 'keys', 'private.pem')
                public_key_path = os.path.join(BASE_DIR, 'keys', 'public.pem')

                json_report, pdf_report = generate_report(
                    file_path=file_path,
                    file_hash=file_hash,
                    private_key_path=private_key_path,
                    public_key_path=public_key_path
                )

                from src.wipe_history import save_wipe_record
                record = {
                    "file_name": os.path.basename(file_path),
                    "file_hash": file_hash,
                    "deleted_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "json_report_path": json_report,
                    "pdf_report_path": pdf_report
                }
                save_wipe_record(record)

                QMessageBox.information(
                    self,
                    "Success",
                    (f"File wiped:\n{file_path}\n\n"
                     f"Reports generated:\n{json_report}\n{pdf_report}\n\n"
                     f"Hash copied above.")
                )
                self.status_panel.setText("File wiped and reports generated. Copy hash and go to Verify.")
            else:
                QMessageBox.warning(self, "Error", f"Could not wipe:\n{file_path}")
                self.status_panel.setText("Wipe failed. Try again.")

    def select_and_wipe_partition(self):
        partition_path = QFileDialog.getExistingDirectory(self, "Select Partition to Wipe")
        if partition_path:
            self.status_panel.setText("Wiping partition...")
            success = wipe_partition(partition_path)
            if success:
                QMessageBox.information(self, "Success", f"Partition wiped:\n{partition_path}")
                self.status_panel.setText("Partition wiped successfully.")
            else:
                QMessageBox.warning(self, "Error", f"Could not wipe partition:\n{partition_path}")
                self.status_panel.setText("Partition wipe failed.")

    def confirm_and_wipe_os(self):
        reply = QMessageBox.warning(
            self,
            "Confirm OS Wipe",
            "This will erase the entire Operating System and all data. This action is irreversible.\nProceed?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.status_panel.setText("Wiping entire OS...")
            success = wipe_os()
            if success:
                QMessageBox.information(self, "Success", "Operating system wiped successfully.")
                self.status_panel.setText("OS wipe completed.")
            else:
                QMessageBox.warning(self, "Error", "Failed to wipe the OS.")
                self.status_panel.setText("OS wipe failed.")

    def compute_file_hash(self, file_path):
        import hashlib
        sha = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha.update(chunk)
        return sha.hexdigest()
