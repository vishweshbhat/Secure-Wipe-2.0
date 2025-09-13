import os
import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox,
    QLineEdit, QHBoxLayout, QProgressBar, QApplication
)
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
                background: #191a1d;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel#header {
                font-size: 28px; font-weight: bold; color: #FFD60A; margin-top: 20px; margin-bottom: 28px;
            }
            QLabel#status {
                font-size: 13px; color: #bbbbbb; background: #181818;
                border-radius: 12px; padding: 10px;
            }
            QPushButton {
                font-size: 20px; font-weight: bold;
                border-radius: 22px;
                min-height: 70px; min-width: 320px;
                margin: 18px 0px;
            }
            QPushButton#btn_file { background: #FFD60A; color: #191a1d;}
            QPushButton#btn_partition { background: #FFD60A; color: #191a1d;}
            QPushButton#btn_os { background: #d32f2f; color: white;}
            QPushButton:hover { filter: brightness(1.2);}
            QLineEdit#hash_display {
                background-color: #202020; color: #FFD60A;
                border-radius: 8px; padding: 5px; font-family: monospace; font-size: 14px;
                margin-bottom: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 10, 0, 12)

        header = QLabel("Secure Wipe Tool")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        self.status_panel = QLabel("Ready. Select a wipe action.")
        self.status_panel.setObjectName("status")
        self.status_panel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_panel)

        # Hash and copy button
        hash_layout = QHBoxLayout()
        self.hash_display = QLineEdit()
        self.hash_display.setObjectName("hash_display")
        self.hash_display.setReadOnly(True)
        self.hash_display.setVisible(False)
        self.copy_hash_btn = QPushButton("Copy Hash")
        self.copy_hash_btn.setVisible(False)
        self.copy_hash_btn.setFixedHeight(30)
        self.copy_hash_btn.clicked.connect(self.copy_hash_to_clipboard)
        hash_layout.addWidget(self.hash_display)
        hash_layout.addWidget(self.copy_hash_btn)
        layout.addLayout(hash_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # BIG BUTTONS WITH ICONS/EMOJIS
        self.select_files_btn = QPushButton("🗑️  Wipe a Specific File")
        self.select_files_btn.setObjectName("btn_file")
        self.select_files_btn.clicked.connect(self.select_and_wipe_file)
        layout.addWidget(self.select_files_btn, alignment=Qt.AlignHCenter)

        self.select_partition_btn = QPushButton("💽  Wipe an Entire Partition")
        self.select_partition_btn.setObjectName("btn_partition")
        self.select_partition_btn.clicked.connect(self.select_and_wipe_partition)
        layout.addWidget(self.select_partition_btn, alignment=Qt.AlignHCenter)

        self.wipe_os_btn = QPushButton("⚠️  Wipe Entire Operating System")
        self.wipe_os_btn.setObjectName("btn_os")
        self.wipe_os_btn.clicked.connect(self.confirm_and_wipe_os)
        layout.addWidget(self.wipe_os_btn, alignment=Qt.AlignHCenter)

    def copy_hash_to_clipboard(self):
        QApplication.clipboard().setText(self.hash_display.text())
        QMessageBox.information(self, "Copied", "File hash copied to clipboard.")

    def select_and_wipe_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Wipe")
        if file_path:
            self.status_panel.setText("Computing file hash...")
            QApplication.processEvents()
            file_hash = self.compute_file_hash(file_path)
            self.hash_display.setText(file_hash)
            self.hash_display.setVisible(True)
            self.copy_hash_btn.setVisible(False)
            self.status_panel.setText("Hash ready. Starting wipe...")
            QApplication.processEvents()

            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)

            success = wipe_file(file_path)
            self.progress_bar.setVisible(False)

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

                record = {
                    "file_name": os.path.basename(file_path),
                    "file_hash": file_hash,
                    "deleted_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "json_report_path": json_report,
                    "pdf_report_path": pdf_report
                }
                save_wipe_record(record)

                self.file_hash = file_hash
                self.copy_hash_btn.setVisible(True)
                QMessageBox.information(self, "Success", (f"File wiped:\n{file_path}\n\nReports generated:\n{json_report}\n{pdf_report}\n\nHash copied above."))
                self.status_panel.setText("File wiped and reports generated. Copy hash and go to Verify.")
            else:
                QMessageBox.warning(self, "Error", f"Could not wipe:\n{file_path}")
                self.status_panel.setText("Wipe failed. Try again.")

    def select_and_wipe_partition(self):
        partition_path = QFileDialog.getExistingDirectory(self, "Select Partition to Wipe")
        if partition_path:
            self.status_panel.setText("Wiping partition...")
            QApplication.processEvents()
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            success = wipe_partition(partition_path)
            self.progress_bar.setVisible(False)
            if success:
                QMessageBox.information(self, "Success", f"Partition wiped:\n{partition_path}")
                self.status_panel.setText("Partition wiped successfully.")
            else:
                QMessageBox.warning(self, "Error", f"Could not wipe partition:\n{partition_path}")
                self.status_panel.setText("Partition wipe failed.")

    def confirm_and_wipe_os(self):
        reply = QMessageBox.warning(self, "Confirm OS Wipe", "This will erase the entire Operating System and all data. This action is irreversible.\nProceed?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.status_panel.setText("Wiping entire OS...")
            QApplication.processEvents()
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            success = wipe_os()
            self.progress_bar.setVisible(False)
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
