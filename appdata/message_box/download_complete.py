# \appdata\message_box\download_complete.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class DownloadCompleteWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Download Complete")
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Download Complete!")
        layout.addWidget(label)
        ok_button = QPushButton("OK")
        layout.addWidget(ok_button)
        ok_button.clicked.connect(self.close)
