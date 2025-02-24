# \appdata\gui\dreambot_edit_account.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox,
    QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from appdata.logic.dreambot_edit_account import DreamBotEditAccountLogic

class DreamBotEditAccountWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamBot Edit Account")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        form_layout = QFormLayout()

        self.account_input = QLineEdit()
        self.account_input.setReadOnly(True)
        self.account_input.setStyleSheet("background-color: #3c3c3c; color: #ececec;")
        form_layout.addRow("Account:", self.account_input)

        self.proxy_combo = QComboBox()
        form_layout.addRow("Select Proxy:", self.proxy_combo)

        self.task_combo = QComboBox()
        form_layout.addRow("Select Task:", self.task_combo)

        self.world_combo = QComboBox()
        form_layout.addRow("Select World:", self.world_combo)

        self.notes_edit = QLineEdit()
        form_layout.addRow("Notes:", self.notes_edit)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.logic = DreamBotEditAccountLogic(self)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
