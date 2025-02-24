# \appdata\gui\general_settings.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from appdata.logic.general_settings import GeneralSettingsLogic

class GeneralSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("General Settings")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        dreambot_label = QLabel("DreamBot Login Details")
        main_layout.addWidget(dreambot_label)
        dreambot_form = QFormLayout()
        self.dreambot_username_input = QLineEdit()
        dreambot_form.addRow("DreamBot Username:", self.dreambot_username_input)
        self.dreambot_password_input = QLineEdit()
        self.dreambot_password_input.setEchoMode(QLineEdit.Password)
        dreambot_form.addRow("DreamBot Password:", self.dreambot_password_input)
        main_layout.addLayout(dreambot_form)

        osbot_label = QLabel("OSBot Login Details")
        main_layout.addWidget(osbot_label)
        osbot_form = QFormLayout()
        self.osbot_username_input = QLineEdit()
        osbot_form.addRow("OSBot Username:", self.osbot_username_input)
        self.osbot_password_input = QLineEdit()
        self.osbot_password_input.setEchoMode(QLineEdit.Password)
        osbot_form.addRow("OSBot Password:", self.osbot_password_input)
        main_layout.addLayout(osbot_form)

        tribot_label = QLabel("TRiBot Login Details")
        main_layout.addWidget(tribot_label)
        tribot_form = QFormLayout()
        self.tribot_username_input = QLineEdit()
        tribot_form.addRow("TRiBot Username:", self.tribot_username_input)
        self.tribot_password_input = QLineEdit()
        self.tribot_password_input.setEchoMode(QLineEdit.Password)
        tribot_form.addRow("TRiBot Password:", self.tribot_password_input)
        main_layout.addLayout(tribot_form)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.logic = GeneralSettingsLogic(self)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
