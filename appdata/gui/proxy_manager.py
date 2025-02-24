# \appdata\gui\proxy_manager.py

import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
)
from appdata.logic.proxy_manager import ProxyManagerLogic

def load_proxies_for_dropdown():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    path = f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\proxies.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except:
        return []

class ProxyManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proxy Manager")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # --------------------------
        # Add Proxy Tab
        # --------------------------
        add_proxy_tab = QWidget()
        add_proxy_layout = QVBoxLayout()
        add_proxy_tab.setLayout(add_proxy_layout)

        add_form_layout = QFormLayout()
        self.ip_input = QLineEdit()
        add_form_layout.addRow("IP Address:", self.ip_input)

        self.port_input = QLineEdit()
        add_form_layout.addRow("Port:", self.port_input)

        self.username_input = QLineEdit()
        add_form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        add_form_layout.addRow("Password:", self.password_input)

        add_proxy_layout.addLayout(add_form_layout)

        add_btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        add_btn_layout.addWidget(self.save_button)
        add_btn_layout.addWidget(self.cancel_button)
        add_proxy_layout.addLayout(add_btn_layout)

        tab_widget.addTab(add_proxy_tab, "Add Proxy")

        # --------------------------
        # Bulk Import Tab
        # --------------------------
        bulk_tab = QWidget()
        bulk_layout = QVBoxLayout()
        bulk_tab.setLayout(bulk_layout)

        self.bulk_text_edit = QTextEdit()
        self.bulk_text_edit.setPlaceholderText("ip:port:username:password")
        bulk_layout.addWidget(self.bulk_text_edit)

        bulk_btn_layout = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.bulk_cancel_button = QPushButton("Cancel")
        bulk_btn_layout.addWidget(self.import_button)
        bulk_btn_layout.addWidget(self.bulk_cancel_button)
        bulk_layout.addLayout(bulk_btn_layout)

        tab_widget.addTab(bulk_tab, "Bulk Import")

        # --------------------------
        # Edit Proxy Tab (New)
        # --------------------------
        edit_tab = QWidget()
        edit_tab_layout = QVBoxLayout()
        edit_tab.setLayout(edit_tab_layout)

        edit_form_layout = QFormLayout()

        self.edit_proxy_combo = QComboBox()
        edit_form_layout.addRow("Select Proxy:", self.edit_proxy_combo)

        self.edit_ip_input = QLineEdit()
        edit_form_layout.addRow("IP Address:", self.edit_ip_input)

        self.edit_port_input = QLineEdit()
        edit_form_layout.addRow("Port:", self.edit_port_input)

        self.edit_username_input = QLineEdit()
        edit_form_layout.addRow("Username:", self.edit_username_input)

        self.edit_password_input = QLineEdit()
        edit_form_layout.addRow("Password:", self.edit_password_input)

        edit_tab_layout.addLayout(edit_form_layout)

        edit_btn_layout = QHBoxLayout()
        self.edit_save_button = QPushButton("Save")
        self.edit_delete_button = QPushButton("Delete")
        self.edit_cancel_button = QPushButton("Cancel")
        edit_btn_layout.addWidget(self.edit_save_button)
        edit_btn_layout.addWidget(self.edit_delete_button)
        edit_btn_layout.addWidget(self.edit_cancel_button)
        edit_tab_layout.addLayout(edit_btn_layout)

        tab_widget.addTab(edit_tab, "Edit Proxy")

        self.logic = ProxyManagerLogic(self)
        self.refresh_proxy_combo()

    def refresh_proxy_combo(self):
        """
        Clears and repopulates the edit_proxy_combo from proxies.json
        based on the 'ip' key.
        """
        self.edit_proxy_combo.clear()
        proxies = load_proxies_for_dropdown()
        for p in proxies:
            if "ip" in p:
                self.edit_proxy_combo.addItem(p["ip"])

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
