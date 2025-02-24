# \appdata\logic\osbot_tasks.py

import os
import json
from PySide6.QtWidgets import QMessageBox

def get_tasks_osbot_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\tasks_osbot.json"

def load_tasks_osbot():
    path = get_tasks_osbot_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_tasks_osbot(tasks):
    path = get_tasks_osbot_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

class OsbotTasksLogic:
    def __init__(self, gui):
        self.gui = gui
        self.connect_signals()
    
    def connect_signals(self):
        self.gui.save_button.clicked.connect(self.handle_save)
        self.gui.cancel_button.clicked.connect(self.handle_cancel)

    def handle_save(self):
        task_name = self.gui.task_name_input.text().strip()
        script = self.gui.script_id_input.text().strip()
        args = self.gui.args_input.text().strip()

        run_until_stopped = self.gui.run_until_stopped_radio.isChecked()
        run_for_val = self.gui.run_from_input.text().strip()
        run_to_val = self.gui.run_to_input.text().strip()

        loop_val = self.gui.loop_checkbox.isChecked()
        break_from_val = self.gui.break_from_input.text().strip()
        break_to_val = self.gui.break_to_input.text().strip()

        if not task_name:
            QMessageBox.warning(self.gui, "Missing Task Name", "Please enter a task name.")
            return

        tasks = load_tasks_osbot()

        for t in tasks:
            if t.get("task_name") == task_name:
                QMessageBox.information(self.gui, "Duplicate Task", f"Task name '{task_name}' already exists.")
                return

        def to_int(value):
            try:
                return int(value)
            except:
                return 0

        new_entry = {
            "task_name": task_name,
            "script": script,
            "args": args,
            "run_until_stopped": run_until_stopped,
            "run_for": to_int(run_for_val),
            "run_to": to_int(run_to_val),
            "loop": loop_val,
            "break_for": to_int(break_from_val),
            "break_to": to_int(break_to_val)
        }

        tasks.append(new_entry)
        save_tasks_osbot(tasks)
        QMessageBox.information(self.gui, "Saved", f"Task '{task_name}' saved.")
        self.clear_fields()

    def handle_cancel(self):
        self.gui.close()

    def clear_fields(self):
        self.gui.task_name_input.clear()
        self.gui.script_id_input.clear()
        self.gui.args_input.clear()
        self.gui.run_until_stopped_radio.setChecked(True)
        self.gui.run_for_radio.setChecked(False)
        self.gui.run_from_input.clear()
        self.gui.run_to_input.clear()
        self.gui.loop_checkbox.setChecked(False)
        self.gui.break_from_input.clear()
        self.gui.break_to_input.clear()
