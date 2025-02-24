# \appdata\logic\proxy_manager.py

import os
import json
from PySide6.QtWidgets import QMessageBox

def get_proxies_json_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\proxies.json"

def load_proxies():
    path = get_proxies_json_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_proxies(proxies):
    path = get_proxies_json_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(proxies, f, indent=2)

class ProxyManagerLogic:
    def __init__(self, gui):
        self.gui = gui
        self.connect_signals()

    def connect_signals(self):
        # Add Proxy Tab
        self.gui.save_button.clicked.connect(self.handle_save)
        self.gui.cancel_button.clicked.connect(self.handle_cancel_add_tab)

        # Bulk Import Tab
        self.gui.import_button.clicked.connect(self.handle_import)
        self.gui.bulk_cancel_button.clicked.connect(self.handle_cancel_bulk_tab)

        # Edit Proxy Tab
        self.gui.edit_proxy_combo.currentIndexChanged.connect(self.handle_edit_select)
        self.gui.edit_save_button.clicked.connect(self.handle_edit_save)
        self.gui.edit_delete_button.clicked.connect(self.handle_edit_delete)
        self.gui.edit_cancel_button.clicked.connect(self.handle_cancel_edit_tab)

    # --------------------------------------
    # CANCEL Buttons (Close window)
    # --------------------------------------
    def handle_cancel_add_tab(self):
        self.gui.close()

    def handle_cancel_bulk_tab(self):
        self.gui.close()

    def handle_cancel_edit_tab(self):
        self.gui.close()

    # --------------------------------------
    # ADD PROXY TAB
    # --------------------------------------
    def handle_save(self):
        ip = self.gui.ip_input.text().strip()
        port = self.gui.port_input.text().strip()
        username = self.gui.username_input.text().strip()
        password = self.gui.password_input.text().strip()

        if not ip or not port:
            QMessageBox.warning(self.gui, "Incomplete Data", "IP Address and Port are required.")
            return

        proxies = load_proxies()
        for p in proxies:
            if p["ip"] == ip:
                QMessageBox.information(self.gui, "Duplicate Proxy", f"IP '{ip}' already exists.")
                return

        new_proxy = {
            "ip": ip,
            "port": port,
            "username": username,
            "password": password
        }
        proxies.append(new_proxy)
        save_proxies(proxies)
        QMessageBox.information(self.gui, "Saved", f"Proxy '{ip}' saved.")
        self.gui.ip_input.clear()
        self.gui.port_input.clear()
        self.gui.username_input.clear()
        self.gui.password_input.clear()

        # Refresh combo in case user wants to edit newly added proxy
        self.gui.refresh_proxy_combo()

    # --------------------------------------
    # BULK IMPORT TAB
    # --------------------------------------
    def handle_import(self):
        lines = self.gui.bulk_text_edit.toPlainText().strip().split("\n")
        if not lines:
            QMessageBox.warning(self.gui, "No Data", "No lines to import.")
            return

        proxies = load_proxies()
        existing_ips = set(p["ip"] for p in proxies)
        bad_format_count = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) != 4:
                bad_format_count += 1
                continue

            ip, port, user, pwd = parts
            ip = ip.strip()
            port = port.strip()
            user = user.strip()
            pwd = pwd.strip()

            if not ip or not port:
                bad_format_count += 1
                continue

            if ip in existing_ips:
                continue

            new_proxy = {
                "ip": ip,
                "port": port,
                "username": user,
                "password": pwd
            }
            proxies.append(new_proxy)
            existing_ips.add(ip)

        save_proxies(proxies)

        if bad_format_count > 0:
            QMessageBox.information(self.gui, "Import Finished",
                                    f"{bad_format_count} line(s) skipped due to bad format.")
        else:
            QMessageBox.information(self.gui, "Import Finished", "All lines successfully imported.")

        self.gui.bulk_text_edit.clear()

        # Refresh the combo in case user wants to edit newly imported proxies
        self.gui.refresh_proxy_combo()

    # --------------------------------------
    # EDIT PROXY TAB
    # --------------------------------------
    def handle_edit_select(self, index):
        if index < 0:
            return
        selected_ip = self.gui.edit_proxy_combo.itemText(index)
        proxies = load_proxies()
        for proxy in proxies:
            if proxy["ip"] == selected_ip:
                self.gui.edit_ip_input.setText(proxy["ip"])
                self.gui.edit_port_input.setText(proxy["port"])
                self.gui.edit_username_input.setText(proxy["username"])
                self.gui.edit_password_input.setText(proxy["password"])
                break

    def handle_edit_save(self):
        selected_index = self.gui.edit_proxy_combo.currentIndex()
        if selected_index < 0:
            return

        old_ip = self.gui.edit_proxy_combo.itemText(selected_index)
        new_ip = self.gui.edit_ip_input.text().strip()
        new_port = self.gui.edit_port_input.text().strip()
        new_user = self.gui.edit_username_input.text().strip()
        new_pwd = self.gui.edit_password_input.text().strip()

        if not new_ip or not new_port:
            QMessageBox.warning(self.gui, "Incomplete Data", "IP Address and Port are required.")
            return

        proxies = load_proxies()
        found_index = None
        for i, p in enumerate(proxies):
            if p["ip"] == old_ip:
                found_index = i
                break

        if found_index is None:
            QMessageBox.warning(self.gui, "Not Found", f"Original IP '{old_ip}' not found in JSON.")
            return

        # If changing IP, check if new IP already exists in another proxy
        if new_ip != old_ip:
            for p in proxies:
                if p["ip"] == new_ip:
                    QMessageBox.information(self.gui, "Duplicate Proxy", f"IP '{new_ip}' already exists.")
                    return

        # Update
        proxies[found_index]["ip"] = new_ip
        proxies[found_index]["port"] = new_port
        proxies[found_index]["username"] = new_user
        proxies[found_index]["password"] = new_pwd

        save_proxies(proxies)
        QMessageBox.information(self.gui, "Saved", f"Proxy '{old_ip}' updated.")

        # Update the combo item
        self.gui.edit_proxy_combo.setItemText(selected_index, new_ip)

    def handle_edit_delete(self):
        selected_index = self.gui.edit_proxy_combo.currentIndex()
        if selected_index < 0:
            return

        selected_ip = self.gui.edit_proxy_combo.itemText(selected_index)

        proxies = load_proxies()
        original_len = len(proxies)
        new_list = [p for p in proxies if p["ip"] != selected_ip]

        if len(new_list) == original_len:
            QMessageBox.information(self.gui, "Not Found", f"IP '{selected_ip}' not found in JSON.")
            return

        save_proxies(new_list)
        QMessageBox.information(self.gui, "Deleted", f"Proxy '{selected_ip}' was deleted.")

        self.gui.refresh_proxy_combo()

        # Clear out the edit fields
        self.gui.edit_ip_input.clear()
        self.gui.edit_port_input.clear()
        self.gui.edit_username_input.clear()
        self.gui.edit_password_input.clear()