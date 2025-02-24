# \appdata\gui\account_manager.py

import os
import json
from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QCheckBox, QPushButton, QTextEdit, QFormLayout, QComboBox
)
from appdata.logic.account_manager import AccountManagerLogic

def load_accounts_for_dropdown():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    path = f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\accounts.json"
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except:
        return []

class AccountsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Account Manager")
        self.init_ui()
        self.logic = AccountManagerLogic(self)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # ---------------------------
        # Add Account Tab
        # ---------------------------
        add_tab = QWidget()
        add_layout = QVBoxLayout()
        add_tab.setLayout(add_layout)
        
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        form_layout.addRow("Username/Email:", self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)
        
        self.pin_input = QLineEdit()
        form_layout.addRow("Pin:", self.pin_input)
        
        self.jagex_checkbox = QCheckBox("Jagex Account")
        form_layout.addRow(self.jagex_checkbox)
        
        add_layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)
        add_layout.addLayout(btn_layout)
        
        tab_widget.addTab(add_tab, "Add Account")

        # ---------------------------
        # Bulk Import Tab
        # ---------------------------
        bulk_tab = QWidget()
        bulk_layout = QVBoxLayout()
        bulk_tab.setLayout(bulk_layout)
        
        self.bulk_text_edit = QTextEdit()
        self.bulk_text_edit.setPlaceholderText("username/email:password:pin:true/false")
        bulk_layout.addWidget(self.bulk_text_edit)
        
        self.bulk_info_label = QLabel('The "true/false" indicates whether it is a Jagex account or not.')
        bulk_layout.addWidget(self.bulk_info_label)
        
        bulk_btn_layout = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.bulk_cancel_button = QPushButton("Cancel")
        bulk_btn_layout.addWidget(self.import_button)
        bulk_btn_layout.addWidget(self.bulk_cancel_button)
        bulk_layout.addLayout(bulk_btn_layout)
        
        tab_widget.addTab(bulk_tab, "Bulk Import")

        # ---------------------------
        # Edit Account Tab
        # ---------------------------
        edit_tab = QWidget()
        edit_layout = QVBoxLayout()
        edit_tab.setLayout(edit_layout)

        edit_form_layout = QFormLayout()

        self.select_account_combo = QComboBox()
        edit_form_layout.addRow("Select Account:", self.select_account_combo)

        self.edit_username_input = QLineEdit()
        edit_form_layout.addRow("Username/Email:", self.edit_username_input)

        self.edit_password_input = QLineEdit()
        self.edit_password_input.setEchoMode(QLineEdit.Password)
        edit_form_layout.addRow("Password:", self.edit_password_input)

        self.edit_pin_input = QLineEdit()
        edit_form_layout.addRow("Pin:", self.edit_pin_input)

        self.edit_jagex_checkbox = QCheckBox("Jagex Account")
        edit_form_layout.addRow(self.edit_jagex_checkbox)

        edit_layout.addLayout(edit_form_layout)

        edit_btn_layout = QHBoxLayout()
        self.edit_save_button = QPushButton("Save")
        # NEW: Delete button
        self.edit_delete_button = QPushButton("Delete")
        self.edit_cancel_button = QPushButton("Cancel")

        edit_btn_layout.addWidget(self.edit_save_button)
        edit_btn_layout.addWidget(self.edit_delete_button)
        edit_btn_layout.addWidget(self.edit_cancel_button)
        edit_layout.addLayout(edit_btn_layout)

        tab_widget.addTab(edit_tab, "Edit Account")

        # Populate the combo box
        self.refresh_account_combo()

    def refresh_account_combo(self):
        """
        Clears and repopulates the Select Account combo box
        from the accounts.json file.
        """
        self.select_account_combo.clear()
        accounts_list = load_accounts_for_dropdown()
        for acc in accounts_list:
            if "account" in acc:
                self.select_account_combo.addItem(acc["account"])

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center()
