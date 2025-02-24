# \appdata\logic\dreambot_tasks.py

import os
import json
from PySide6.QtWidgets import QMessageBox

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

def save_tasks_dreambot(tasks):
    path = get_tasks_dreambot_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

class DreamBotTasksLogic:
    def __init__(self, gui):
        self.gui = gui
        self.connect_signals()
    
    def connect_signals(self):
        # Add tab
        self.gui.save_button.clicked.connect(self.handle_add_save)
        self.gui.cancel_button.clicked.connect(self.handle_add_cancel)

        # Edit tab
        self.gui.select_task_combo.currentIndexChanged.connect(self.handle_edit_select)
        self.gui.edit_save_button.clicked.connect(self.handle_edit_save)
        self.gui.edit_delete_button.clicked.connect(self.handle_edit_delete)
        self.gui.edit_cancel_button.clicked.connect(self.handle_edit_cancel)

    # -------------------------------------------------
    # ADD TAB LOGIC
    # -------------------------------------------------
    def handle_add_save(self):
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

        tasks = load_tasks_dreambot()

        # Check for duplicate
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
        save_tasks_dreambot(tasks)
        QMessageBox.information(self.gui, "Saved", f"Task '{task_name}' saved.")
        self.clear_add_fields()

        # Refresh combo in case user wants to edit newly added task
        self.gui.refresh_task_combo()

    def handle_add_cancel(self):
        self.gui.close()

    def clear_add_fields(self):
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

    # -------------------------------------------------
    # EDIT TAB LOGIC
    # -------------------------------------------------
    def handle_edit_select(self, index):
        if index < 0:
            return
        selected_task = self.gui.select_task_combo.itemText(index)
        tasks = load_tasks_dreambot()
        found = None
        for t in tasks:
            if t.get("task_name") == selected_task:
                found = t
                break

        if not found:
            return

        self.gui.edit_task_name_input.setText(found.get("task_name", ""))
        self.gui.edit_script_id_input.setText(found.get("script", ""))
        self.gui.edit_args_input.setText(found.get("args", ""))

        # Radio buttons for run_until_stopped vs run_for
        run_until = found.get("run_until_stopped", True)
        self.gui.edit_run_until_stopped_radio.setChecked(run_until)
        self.gui.edit_run_for_radio.setChecked(not run_until)

        self.gui.edit_run_from_input.setText(str(found.get("run_for", 0)))
        self.gui.edit_run_to_input.setText(str(found.get("run_to", 0)))

        self.gui.edit_loop_checkbox.setChecked(bool(found.get("loop", False)))
        self.gui.edit_break_from_input.setText(str(found.get("break_for", 0)))
        self.gui.edit_break_to_input.setText(str(found.get("break_to", 0)))

    def handle_edit_save(self):
        selected_index = self.gui.select_task_combo.currentIndex()
        if selected_index < 0:
            return

        old_task_name = self.gui.select_task_combo.itemText(selected_index)

        new_task_name = self.gui.edit_task_name_input.text().strip()
        new_script = self.gui.edit_script_id_input.text().strip()
        new_args = self.gui.edit_args_input.text().strip()

        run_until_stopped = self.gui.edit_run_until_stopped_radio.isChecked()
        run_for_val = self.gui.edit_run_from_input.text().strip()
        run_to_val = self.gui.edit_run_to_input.text().strip()

        loop_val = self.gui.edit_loop_checkbox.isChecked()
        break_from_val = self.gui.edit_break_from_input.text().strip()
        break_to_val = self.gui.edit_break_to_input.text().strip()

        if not new_task_name:
            QMessageBox.warning(self.gui, "Missing Task Name", "Please enter a task name.")
            return

        tasks = load_tasks_dreambot()
        found_index = None
        for i, t in enumerate(tasks):
            if t.get("task_name") == old_task_name:
                found_index = i
                break

        if found_index is None:
            QMessageBox.warning(self.gui, "Not Found", f"Task '{old_task_name}' not found in JSON.")
            return

        # If user changes the task_name, ensure it's not duplicating another
        if new_task_name != old_task_name:
            for t in tasks:
                if t.get("task_name") == new_task_name:
                    QMessageBox.information(self.gui, "Duplicate Task",
                                            f"Task name '{new_task_name}' already exists.")
                    return

        def to_int(value):
            try:
                return int(value)
            except:
                return 0

        # Update
        tasks[found_index]["task_name"] = new_task_name
        tasks[found_index]["script"] = new_script
        tasks[found_index]["args"] = new_args
        tasks[found_index]["run_until_stopped"] = run_until_stopped
        tasks[found_index]["run_for"] = to_int(run_for_val)
        tasks[found_index]["run_to"] = to_int(run_to_val)
        tasks[found_index]["loop"] = loop_val
        tasks[found_index]["break_for"] = to_int(break_from_val)
        tasks[found_index]["break_to"] = to_int(break_to_val)

        save_tasks_dreambot(tasks)
        QMessageBox.information(self.gui, "Saved", f"Task '{old_task_name}' updated.")

        # Update combo box text
        self.gui.select_task_combo.setItemText(selected_index, new_task_name)

    def handle_edit_delete(self):
        selected_index = self.gui.select_task_combo.currentIndex()
        if selected_index < 0:
            return

        old_task_name = self.gui.select_task_combo.itemText(selected_index)
        tasks = load_tasks_dreambot()

        new_list = [t for t in tasks if t.get("task_name") != old_task_name]
        if len(new_list) == len(tasks):
            QMessageBox.information(self.gui, "Not Found", f"Task '{old_task_name}' not found in JSON.")
            return

        save_tasks_dreambot(new_list)
        QMessageBox.information(self.gui, "Deleted", f"Task '{old_task_name}' was deleted.")

        # Refresh combo
        self.gui.refresh_task_combo()
        self.clear_edit_fields()

    def handle_edit_cancel(self):
        self.gui.close()

    def clear_edit_fields(self):
        self.gui.edit_task_name_input.clear()
        self.gui.edit_script_id_input.clear()
        self.gui.edit_args_input.clear()
        self.gui.edit_run_until_stopped_radio.setChecked(True)
        self.gui.edit_run_for_radio.setChecked(False)
        self.gui.edit_run_from_input.clear()
        self.gui.edit_run_to_input.clear()
        self.gui.edit_loop_checkbox.setChecked(False)
        self.gui.edit_break_from_input.clear()
        self.gui.edit_break_to_input.clear()
