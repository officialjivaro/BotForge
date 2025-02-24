# \appdata\logic\general_settings.py

import os
import json
from PySide6.QtWidgets import QMessageBox

def get_general_settings_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\general_settings.json"

def load_general_settings():
    path = get_general_settings_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_general_settings(data_list):
    path = get_general_settings_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2)

class GeneralSettingsLogic:
    def __init__(self, gui):
        self.gui = gui
        self.connect_signals()
        self.populate_fields()

    def connect_signals(self):
        self.gui.save_button.clicked.connect(self.handle_save)
        self.gui.cancel_button.clicked.connect(self.handle_cancel)

    def populate_fields(self):
        data_list = load_general_settings()
        # In case the file is missing or invalid, data_list is an empty list

        # We'll search for the "client" objects
        # for dreambot, osbot, tribot, and set the matching fields
        for obj in data_list:
            c = obj.get("client", "").lower()
            if c == "dreambot":
                self.gui.dreambot_username_input.setText(obj.get("dreambot_username", ""))
                self.gui.dreambot_password_input.setText(obj.get("dreambot_password", ""))
            elif c == "osbot":
                self.gui.osbot_username_input.setText(obj.get("osbot_username", ""))
                self.gui.osbot_password_input.setText(obj.get("osbot_password", ""))
            elif c == "tribot":
                self.gui.tribot_username_input.setText(obj.get("tribot_username", ""))
                self.gui.tribot_password_input.setText(obj.get("tribot_password", ""))

    def handle_save(self):
        dreambot_user = self.gui.dreambot_username_input.text().strip()
        dreambot_pass = self.gui.dreambot_password_input.text().strip()
        osbot_user = self.gui.osbot_username_input.text().strip()
        osbot_pass = self.gui.osbot_password_input.text().strip()
        tribot_user = self.gui.tribot_username_input.text().strip()
        tribot_pass = self.gui.tribot_password_input.text().strip()

        data_list = load_general_settings()

        # Remove existing dreambot/osbot/tribot objects
        data_list = [obj for obj in data_list if obj.get("client") not in ["dreambot", "osbot", "tribot"]]

        # Append dreambot object
        data_list.append({
            "client": "dreambot",
            "dreambot_username": dreambot_user,
            "dreambot_password": dreambot_pass
        })

        # Append osbot object
        data_list.append({
            "client": "osbot",
            "osbot_username": osbot_user,
            "osbot_password": osbot_pass
        })

        # Append tribot object
        data_list.append({
            "client": "tribot",
            "tribot_username": tribot_user,
            "tribot_password": tribot_pass
        })

        save_general_settings(data_list)
        QMessageBox.information(self.gui, "Saved", "General settings saved successfully.")

    def handle_cancel(self):
        self.gui.close()
