# \appdata\logic\datagridview_populate.py

import os
import json
import getpass
from PySide6.QtGui import QStandardItem

def get_accounts_json_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\accounts.json"

def populate_datagridview(model, task_key="tribot_task"):
    """
    Populates the provided QStandardItemModel with rows from the JSON file.

    Columns: [Account, Proxy, Task, World, Notes, Status]
    The 'task_key' parameter can be changed to "dreambot_task", "osbot_task", etc.
    """
    model.removeRows(0, model.rowCount())
    
    path = get_accounts_json_path()
    if not os.path.exists(path):
        return
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return
    
    if not isinstance(data, list):
        return

    for record in data:
        account = record.get("account", "")
        proxy = record.get("proxy", "")
        task = record.get(task_key, "")
        world = record.get("world", "")
        notes = record.get("notes", "")
        
        # 'status' can be left blank for now
        status = ""

        row_items = [
            QStandardItem(str(account)),
            QStandardItem(str(proxy)),
            QStandardItem(str(task)),
            QStandardItem(str(world)),
            QStandardItem(str(notes)),
            QStandardItem(str(status))
        ]
        model.appendRow(row_items)
