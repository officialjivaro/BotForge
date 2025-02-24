# \appdata\logic\account_manager.py

import os
import json
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer

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

def save_accounts(accounts):
    path = get_accounts_json_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)

class AccountManagerLogic:
    def __init__(self, gui):
        self.gui = gui
        self.connect_signals()

    def connect_signals(self):
        # Existing signals for Add and Bulk Import tabs
        self.gui.save_button.clicked.connect(self.handle_save)
        self.gui.import_button.clicked.connect(self.handle_import)

        # Signals for the Edit Account tab
        self.gui.select_account_combo.currentIndexChanged.connect(self.handle_edit_select)
        self.gui.edit_save_button.clicked.connect(self.handle_edit_save)
        self.gui.edit_delete_button.clicked.connect(self.handle_edit_delete)  # NEW
        self.gui.edit_cancel_button.clicked.connect(self.handle_edit_cancel)

    def handle_save(self):
        account = self.gui.username_input.text().strip()
        password = self.gui.password_input.text().strip()
        pin = self.gui.pin_input.text().strip()
        jagex_account = self.gui.jagex_checkbox.isChecked()

        if not account or not password:
            QMessageBox.warning(self.gui, "Incomplete Data", "Username/Email and Password are required.")
            return

        accounts = load_accounts()
        for acc in accounts:
            if acc["account"] == account:
                QMessageBox.information(self.gui, "Duplicate Account", f"Account '{account}' already exists.")
                return

        new_entry = {
            "account": account,
            "password": password,
            "pin": pin,
            "jagex_account": jagex_account,
            "proxy": "",
            "dreambot_task": "",
            "osbot_task": "",
            "tribot_task": "",
            "world": "f2p",
            "notes": ""
        }

        accounts.append(new_entry)
        save_accounts(accounts)
        QMessageBox.information(self.gui, "Saved", f"Account '{account}' saved.")
        self.gui.username_input.clear()
        self.gui.password_input.clear()
        self.gui.pin_input.clear()
        self.gui.jagex_checkbox.setChecked(False)

        # Also refresh the combo in case user wants to edit newly added account
        self.gui.refresh_account_combo()

    def handle_import(self):
        lines = self.gui.bulk_text_edit.toPlainText().strip().split("\n")
        if not lines:
            QMessageBox.warning(self.gui, "No Data", "No lines to import.")
            return

        accounts = load_accounts()
        existing_accounts = set(acc["account"] for acc in accounts)

        bad_format_count = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) != 4:
                bad_format_count += 1
                continue

            acc_user, acc_pass, acc_pin, acc_jagex_str = parts
            acc_user = acc_user.strip()
            acc_pass = acc_pass.strip()
            acc_pin = acc_pin.strip()
            acc_jagex_str = acc_jagex_str.strip().lower()

            if not acc_user or not acc_pass:
                bad_format_count += 1
                continue

            if acc_jagex_str not in ["true", "false"]:
                bad_format_count += 1
                continue

            jagex_bool = (acc_jagex_str == "true")

            if acc_user in existing_accounts:
                continue

            new_entry = {
                "account": acc_user,
                "password": acc_pass,
                "pin": acc_pin,
                "jagex_account": jagex_bool,
                "proxy": "",
                "dreambot_task": "",
                "osbot_task": "",
                "tribot_task": "",
                "world": "f2p",
                "notes": ""
            }

            accounts.append(new_entry)
            existing_accounts.add(acc_user)

        save_accounts(accounts)

        if bad_format_count > 0:
            QMessageBox.information(self.gui, "Import Finished",
                                    f"Some lines had the wrong format. {bad_format_count} line(s) skipped.")
        else:
            QMessageBox.information(self.gui, "Import Finished", "All lines successfully imported.")

        self.gui.bulk_text_edit.clear()
        # Refresh the combo to reflect newly imported accounts
        self.gui.refresh_account_combo()

    # ----------------------------------------------------------------
    # EDIT ACCOUNT TAB LOGIC
    # ----------------------------------------------------------------
    def handle_edit_select(self, index):
        if index < 0:
            return
        selected_account = self.gui.select_account_combo.itemText(index)
        accounts = load_accounts()
        for acc in accounts:
            if acc["account"] == selected_account:
                self.gui.edit_username_input.setText(acc["account"])
                self.gui.edit_password_input.setText(acc["password"])
                self.gui.edit_pin_input.setText(acc["pin"])
                self.gui.edit_jagex_checkbox.setChecked(bool(acc["jagex_account"]))
                break

    def handle_edit_save(self):
        selected_index = self.gui.select_account_combo.currentIndex()
        if selected_index < 0:
            return
        old_account_name = self.gui.select_account_combo.itemText(selected_index)

        new_account_name = self.gui.edit_username_input.text().strip()
        new_password = self.gui.edit_password_input.text().strip()
        new_pin = self.gui.edit_pin_input.text().strip()
        new_jagex = self.gui.edit_jagex_checkbox.isChecked()

        if not new_account_name or not new_password:
            QMessageBox.warning(self.gui, "Incomplete Data", "Username/Email and Password are required.")
            return

        accounts = load_accounts()
        found_index = None
        for i, acc in enumerate(accounts):
            if acc["account"] == old_account_name:
                found_index = i
                break

        if found_index is None:
            QMessageBox.warning(self.gui, "Not Found", "Original account not found in JSON.")
            return

        # Check if new_account_name is conflicting with some other account
        if new_account_name != old_account_name:
            for acc in accounts:
                if acc["account"] == new_account_name:
                    QMessageBox.information(self.gui, "Duplicate Account", f"Account '{new_account_name}' already exists.")
                    return

        accounts[found_index]["account"] = new_account_name
        accounts[found_index]["password"] = new_password
        accounts[found_index]["pin"] = new_pin
        accounts[found_index]["jagex_account"] = new_jagex

        save_accounts(accounts)
        QMessageBox.information(self.gui, "Saved", f"Account '{old_account_name}' updated.")

        # Update the combo box item text
        self.gui.select_account_combo.setItemText(selected_index, new_account_name)

    def handle_edit_delete(self):
        """
        Deletes the selected account from accounts.json
        and refreshes the combo so it no longer appears.
        """
        selected_index = self.gui.select_account_combo.currentIndex()
        if selected_index < 0:
            return

        selected_account = self.gui.select_account_combo.itemText(selected_index)

        accounts = load_accounts()
        original_len = len(accounts)
        new_accounts = [acc for acc in accounts if acc["account"] != selected_account]

        if len(new_accounts) == original_len:
            # Means we didn't actually remove anything
            QMessageBox.information(self.gui, "Not Found", f"Account '{selected_account}' not found in JSON.")
            return

        # Save updated list
        save_accounts(new_accounts)
        QMessageBox.information(self.gui, "Deleted", f"Account '{selected_account}' was deleted.")

        # Refresh the combo box and fields
        self.gui.refresh_account_combo()

        # Clear out the edit fields
        self.gui.edit_username_input.clear()
        self.gui.edit_password_input.clear()
        self.gui.edit_pin_input.clear()
        self.gui.edit_jagex_checkbox.setChecked(False)

    def handle_edit_cancel(self):
        self.gui.close()
