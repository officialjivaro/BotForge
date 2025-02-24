# \appdata\logic\tribot_manager.py

import os
import json
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from appdata.gui.tribot_edit_account import TribotEditAccountWindow

def get_accounts_json_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\accounts.json"

def load_accounts():
    path = get_accounts_json_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

class TRiBotManagerLogic:
    def __init__(self, gui):
        self.gui = gui
        self.edit_window = None
        self.connect_signals()

    def connect_signals(self):
        self.gui.edit_button.clicked.connect(self.handle_edit_clicked)

    def handle_edit_clicked(self):
        selected = self.gui.table_view.selectionModel().selectedRows()
        if len(selected) == 0:
            QMessageBox.information(self.gui, "No Selection", "Please select one row first.")
            return
        if len(selected) > 1:
            QMessageBox.information(self.gui, "Multiple Selection", "Please select only one row.")
            return

        row = selected[0].row()
        account = self.gui.model.item(row, 0).text()

        data = load_accounts()
        record = None
        for acc in data:
            if acc.get("account") == account:
                record = acc
                break
        if not record:
            QMessageBox.information(self.gui, "Not Found", f"Account '{account}' not found in JSON.")
            return

        self.edit_window = TribotEditAccountWindow()
        self.populate_edit_window(record)
        self.edit_window.show()

    def populate_edit_window(self, record):
        self.edit_window.account_input.setText(record.get("account", ""))

        proxy_val = record.get("proxy", "")
        self.set_current_text_if_exists(self.edit_window.proxy_combo, proxy_val)

        tribot_task_val = record.get("tribot_task", "")
        self.set_current_text_if_exists(self.edit_window.task_combo, tribot_task_val)

        world_val = record.get("world", "")
        self.set_current_text_if_exists(self.edit_window.world_combo, world_val)

        # Change from setPlainText(...) to setText(...) because 'notes_edit' is now a QLineEdit
        self.edit_window.notes_edit.setText(record.get("notes", ""))

    def set_current_text_if_exists(self, combo, value):
        if not value:
            return
        items = [combo.itemText(i) for i in range(combo.count())]
        if value not in items:
            combo.addItem(value)
        combo.setCurrentText(value)
