# \appdata\logic\dreambot_manager.py

import os
import json
import time
import subprocess
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from appdata.gui.dreambot_edit_account import DreamBotEditAccountWindow
from appdata.gui.dreambot_cli_settings import DreamBotCLISettingsWindow

def get_username():
    try:
        return os.getlogin()
    except:
        return os.environ.get("USERNAME", "default")

def get_accounts_json_path():
    username = get_username()
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\accounts.json"

def get_tasks_dreambot_path():
    username = get_username()
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\tasks_dreambot.json"

def get_cli_settings_path():
    username = get_username()
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\cli_settings.json"

def get_general_settings_path():
    username = get_username()
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\general_settings.json"

def load_json_data(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

class DreamBotManagerLogic:
    def __init__(self, gui):
        self.gui = gui
        self.edit_window = None
        self.cli_settings_window = None
        self.connect_signals()

    def connect_signals(self):
        self.gui.edit_button.clicked.connect(self.handle_edit_clicked)
        self.gui.cli_settings_button.clicked.connect(self.handle_cli_settings_clicked)
        self.gui.run_button.clicked.connect(self.handle_run_clicked)

    def handle_edit_clicked(self):
        selected = self.gui.table_view.selectionModel().selectedRows()
        if len(selected) == 0:
            QMessageBox.information(self.gui, "No Selection", "Please select one row first.")
            return
        if len(selected) > 1:
            QMessageBox.information(self.gui, "Multiple Selection", "Please select only one row.")
            return

        row = selected[0].row()
        account_cell = self.gui.model.item(row, 0).text()

        accounts_data = load_json_data(get_accounts_json_path())
        record = None
        for acc in accounts_data:
            if acc.get("account") == account_cell:
                record = acc
                break
        if not record:
            QMessageBox.information(self.gui, "Not Found", f"Account '{account_cell}' not found in JSON.")
            return

        self.edit_window = DreamBotEditAccountWindow()
        self.populate_edit_window(record)
        self.edit_window.show()

    def populate_edit_window(self, record):
        self.edit_window.account_input.setText(record.get("account", ""))

        proxy_val = record.get("proxy", "")
        self.set_current_text_if_exists(self.edit_window.proxy_combo, proxy_val)

        dreambot_task_val = record.get("dreambot_task", "")
        self.set_current_text_if_exists(self.edit_window.task_combo, dreambot_task_val)

        world_val = record.get("world", "")
        self.set_current_text_if_exists(self.edit_window.world_combo, world_val)

        self.edit_window.notes_edit.setText(record.get("notes", ""))

    def set_current_text_if_exists(self, combo, value):
        if not value:
            return
        items = [combo.itemText(i) for i in range(combo.count())]
        if value not in items:
            combo.addItem(value)
        combo.setCurrentText(value)

    def handle_cli_settings_clicked(self):
        self.cli_settings_window = DreamBotCLISettingsWindow()
        self.cli_settings_window.show()

    def handle_run_clicked(self):
        selected_rows = self.gui.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self.gui, "No Selection", "Please select at least one row.")
            return

        # Load data from various JSON files
        general_settings_data = load_json_data(get_general_settings_path())  
        accounts_data = load_json_data(get_accounts_json_path())  
        tasks_data = load_json_data(get_tasks_dreambot_path())    
        cli_settings_data = load_json_data(get_cli_settings_path())  

        # 1) DreamBot user/pw from general_settings (client=dreambot)
        dreambot_user = ""
        dreambot_pass = ""
        for obj in general_settings_data:
            if obj.get("client") == "dreambot":
                dreambot_user = obj.get("dreambot_username", "")
                dreambot_pass = obj.get("dreambot_password", "")
                break

        # 2) DreamBot CLI settings from cli_settings.json
        dreambot_cli = {}
        for obj in cli_settings_data:
            if obj.get("client") == "dreambot":
                dreambot_cli = obj
                break

        # Paths
        username = get_username()
        java_path = f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\JRE8\\bin\\javaw.exe"
        jar_path = f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\Clients\\DreamBot.jar"

        for index, selected_idx in enumerate(selected_rows):
            row = selected_idx.row()

            account_cell = self.gui.model.item(row, 0).text()  # "Account"
            task_cell = self.gui.model.item(row, 2).text()     # "Task"

            # Find matching account
            account_obj = None
            for acc in accounts_data:
                if acc.get("account") == account_cell:
                    account_obj = acc
                    break

            # Find matching task
            task_obj = None
            for tsk in tasks_data:
                if tsk.get("task_name") == task_cell:
                    task_obj = tsk
                    break

            # Build argument list
            args = []

            # DreamBot credentials
            if dreambot_user:
                args.append(self.arg_with_quotes("-username", dreambot_user))
            if dreambot_pass:
                args.append(self.arg_with_quotes("-password", dreambot_pass))

            # Account-based info
            if account_obj:
                if account_obj.get("jagex_account", False):
                    args.append("-newAccountSystem")

                acc_usr = account_obj.get("account", "")
                acc_pwd = account_obj.get("password", "")
                acc_pin = account_obj.get("pin", "")
                w_val = account_obj.get("world", "").lower()
                if w_val == "p2p":
                    w_val = "members"

                if acc_usr:
                    args.append(self.arg_with_quotes("-accountUsername", acc_usr))
                if acc_pwd:
                    args.append(self.arg_with_quotes("-accountPassword", acc_pwd))
                if acc_pin:
                    args.append(self.arg_with_quotes("-accountPin", acc_pin))
                if w_val:
                    args.append(self.arg_with_quotes("-world", w_val))

            # Task-based info
            if task_obj:
                script_val = task_obj.get("script", "")
                params_val = task_obj.get("args", "")
                if script_val:
                    args.append(self.arg_with_quotes("-script", script_val))
                if params_val:
                    args.append(self.arg_with_quotes("-params", params_val))

            # DreamBot CLI settings
            if dreambot_cli:
                bn = dreambot_cli.get("break_nickname", "").strip()
                if bn:
                    args.append(self.arg_with_quotes("-breaks", bn))
                if dreambot_cli.get("covert_mode", False):
                    args.append("-covert")
                fps_val = dreambot_cli.get("fps", 25)
                args.append(self.arg_with_quotes("-fps", str(fps_val)))
                if dreambot_cli.get("fresh_start", False):
                    args.append("-fresh")
                layout_val = dreambot_cli.get("layout", "fixed")
                args.append(self.arg_with_quotes("-layout", layout_val))
                mouse_val = dreambot_cli.get("mouse_speed", 15)
                args.append(self.arg_with_quotes("-mouse-speed", str(mouse_val)))
                render_val = dreambot_cli.get("render", "all")
                args.append(self.arg_with_quotes("-render", render_val))

            # Final Popen arguments
            final_args = [
                java_path,
                "-jar",
                jar_path,
            ]
            for a in args:
                # a might be something like: '-username "some user"'
                # We'll split once on space to separate the flag from the quoted value
                # Example: a.split(' ', 1) -> ['-username', '"some user"']
                splitted = a.split(' ', 1)
                final_args.extend(splitted)

            # Launch
            try:
                subprocess.Popen(final_args)
            except Exception as e:
                QMessageBox.warning(self.gui, "Launch Error", f"Failed to launch DreamBot instance:\n{str(e)}")

            # 5-second delay if more are selected
            if index < len(selected_rows) - 1:
                time.sleep(5)

    def arg_with_quotes(self, arg_name, arg_value):
        """
        Returns something like: -username "this is my name"
        so that spaces in the value won't break CLI parsing.
        """
        return f'{arg_name} "{arg_value}"'
