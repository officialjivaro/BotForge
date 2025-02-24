# \appdata\logic\dreambot_edit_account.py

import os
import json
from PySide6.QtWidgets import QMessageBox

def get_proxies_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\proxies.json"

def load_proxies():
    path = get_proxies_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_tasks_dreambot_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\tasks_dreambot.json"

def load_tasks_dreambot():
    path = get_tasks_dreambot_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_accounts_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\accounts.json"

def load_accounts():
    path = get_accounts_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_accounts(accounts):
    path = get_accounts_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(accounts, f, indent=2)

world_list = [
    "f2p", "301", "308", "316", "326", "335", "371", "380", "382", "383", "384", "394",
    "397", "398", "399", "417", "418", "430", "431", "433", "434", "435", "436", "437",
    "451", "452", "453", "454", "455", "456", "469", "470", "471", "475", "476", "483",
    "497", "498", "499", "500", "501", "537", "542", "543", "544", "545", "546", "547",
    "552", "553", "554", "555", "556", "557", "562", "563", "571", "575", "members",
    "302", "303", "304", "305", "306", "307", "309", "310", "311", "312", "313", "314",
    "315", "317", "318", "319", "320", "321", "322", "323", "324", "325", "327", "328",
    "329", "330", "331", "332", "333", "334", "336", "337", "338", "339", "340", "341",
    "343", "344", "346", "347", "348", "350", "351", "352", "354", "355", "357", "358",
    "359", "360", "362", "367", "368", "369", "370", "374", "375", "376", "377", "378",
    "386", "387", "388", "389", "390", "395", "421", "422", "424", "443", "444", "445",
    "446", "463", "464", "465", "466", "477", "478", "480", "481", "482", "484", "485",
    "486", "487", "488", "489", "490", "491", "492", "493", "494", "495", "496", "505",
    "506", "507", "508", "509", "510", "511", "512", "513", "514", "515", "516", "517",
    "518", "519", "520", "521", "522", "523", "524", "525", "531", "532", "533", "534",
    "535", "580"
]

class DreamBotEditAccountLogic:
    """
    This class populates combos on init and handles saving/canceling logic for dreambot_edit_account
    """
    def __init__(self, gui):
        self.gui = gui
        self.populate_dropdowns()
        self.connect_signals()

    def populate_dropdowns(self):
        self.populate_proxy_combo()
        self.populate_task_combo()
        self.populate_world_combo()

    def populate_proxy_combo(self):
        proxies = load_proxies()
        for p in proxies:
            ip_val = p.get("ip", "").strip()
            if ip_val:
                self.gui.proxy_combo.addItem(ip_val)

    def populate_task_combo(self):
        tasks = load_tasks_dreambot()
        for t in tasks:
            task_name = t.get("task_name", "").strip()
            if task_name:
                self.gui.task_combo.addItem(task_name)

    def populate_world_combo(self):
        for w in world_list:
            self.gui.world_combo.addItem(str(w))

    def connect_signals(self):
        self.gui.save_button.clicked.connect(self.handle_save)
        self.gui.cancel_button.clicked.connect(self.handle_cancel)

    def handle_save(self):
        account_val = self.gui.account_input.text().strip()
        if not account_val:
            QMessageBox.information(self.gui, "No Account", "No account specified. Nothing to save.")
            return
        
        accounts = load_accounts()
        found = None
        for acc in accounts:
            if acc.get("account") == account_val:
                found = acc
                break
        if not found:
            QMessageBox.information(self.gui, "Not Found", f"Account '{account_val}' not found in accounts.json.")
            return

        # Update keys
        found["proxy"] = self.gui.proxy_combo.currentText().strip()
        # 'dreambot_task' used instead of 'tribot_task'
        found["dreambot_task"] = self.gui.task_combo.currentText().strip()
        found["world"] = self.gui.world_combo.currentText().strip()
        found["notes"] = self.gui.notes_edit.text().strip()

        save_accounts(accounts)
        QMessageBox.information(self.gui, "Saved", "Account updated successfully.")

    def handle_cancel(self):
        self.gui.close()
