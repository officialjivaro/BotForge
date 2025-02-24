# \appdata\gui\dreambot_tasks.py

import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QCheckBox, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt
from appdata.logic.dreambot_tasks import DreamBotTasksLogic

class DreamBotTasksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamBot Task Manager")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # ---------------------------
        # ADD TASK TAB
        # ---------------------------
        add_tab = QWidget()
        add_layout = QVBoxLayout()
        add_tab.setLayout(add_layout)

        add_form = QFormLayout()

        self.task_name_input = QLineEdit()
        add_form.addRow("Task Name:", self.task_name_input)

        self.script_id_input = QLineEdit()
        add_form.addRow("Script Name:", self.script_id_input)

        self.args_input = QLineEdit()
        add_form.addRow("Args/Params:", self.args_input)

        add_layout.addLayout(add_form)

        radio_layout = QHBoxLayout()
        self.run_until_stopped_radio = QRadioButton("Run Script until Stopped")
        self.run_until_stopped_radio.setChecked(True)  # default
        self.run_for_radio = QRadioButton("Run For:")
        radio_layout.addWidget(self.run_until_stopped_radio)
        radio_layout.addWidget(self.run_for_radio)
        add_layout.addLayout(radio_layout)

        run_for_layout = QFormLayout()
        self.run_from_input = QLineEdit()
        self.run_to_input = QLineEdit()
        run_for_layout.addRow("Run From (mins):", self.run_from_input)
        run_for_layout.addRow("To (mins):", self.run_to_input)
        add_layout.addLayout(run_for_layout)

        loop_layout = QHBoxLayout()
        self.loop_checkbox = QCheckBox("Loop")
        loop_layout.addWidget(self.loop_checkbox)
        add_layout.addLayout(loop_layout)

        break_for_layout = QFormLayout()
        self.break_from_input = QLineEdit()
        self.break_to_input = QLineEdit()
        break_for_layout.addRow("Break From (mins):", self.break_from_input)
        break_for_layout.addRow("To (mins):", self.break_to_input)
        add_layout.addLayout(break_for_layout)

        add_button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        add_button_layout.addWidget(self.save_button)
        add_button_layout.addWidget(self.cancel_button)
        add_layout.addLayout(add_button_layout)

        self.tab_widget.addTab(add_tab, "Add Task")

        # ---------------------------
        # EDIT TASK TAB
        # ---------------------------
        edit_tab = QWidget()
        edit_layout = QVBoxLayout()
        edit_tab.setLayout(edit_layout)

        edit_form = QFormLayout()

        self.select_task_combo = QComboBox()
        edit_form.addRow("Select Task:", self.select_task_combo)

        self.edit_task_name_input = QLineEdit()
        edit_form.addRow("Task Name:", self.edit_task_name_input)

        self.edit_script_id_input = QLineEdit()
        edit_form.addRow("Script Name:", self.edit_script_id_input)

        self.edit_args_input = QLineEdit()
        edit_form.addRow("Args/Params:", self.edit_args_input)

        edit_layout.addLayout(edit_form)

        edit_radio_layout = QHBoxLayout()
        self.edit_run_until_stopped_radio = QRadioButton("Run Script until Stopped")
        self.edit_run_for_radio = QRadioButton("Run For:")
        edit_radio_layout.addWidget(self.edit_run_until_stopped_radio)
        edit_radio_layout.addWidget(self.edit_run_for_radio)
        edit_layout.addLayout(edit_radio_layout)

        edit_run_for_layout = QFormLayout()
        self.edit_run_from_input = QLineEdit()
        self.edit_run_to_input = QLineEdit()
        edit_run_for_layout.addRow("Run From (mins):", self.edit_run_from_input)
        edit_run_for_layout.addRow("To (mins):", self.edit_run_to_input)
        edit_layout.addLayout(edit_run_for_layout)

        edit_loop_layout = QHBoxLayout()
        self.edit_loop_checkbox = QCheckBox("Loop")
        edit_loop_layout.addWidget(self.edit_loop_checkbox)
        edit_layout.addLayout(edit_loop_layout)

        edit_break_for_layout = QFormLayout()
        self.edit_break_from_input = QLineEdit()
        self.edit_break_to_input = QLineEdit()
        edit_break_for_layout.addRow("Break From (mins):", self.edit_break_from_input)
        edit_break_for_layout.addRow("To (mins):", self.edit_break_to_input)
        edit_layout.addLayout(edit_break_for_layout)

        edit_button_layout = QHBoxLayout()
        self.edit_save_button = QPushButton("Save")
        self.edit_delete_button = QPushButton("Delete")
        self.edit_cancel_button = QPushButton("Cancel")
        edit_button_layout.addWidget(self.edit_save_button)
        edit_button_layout.addWidget(self.edit_delete_button)
        edit_button_layout.addWidget(self.edit_cancel_button)
        edit_layout.addLayout(edit_button_layout)

        self.tab_widget.addTab(edit_tab, "Edit Task")

        self.logic = DreamBotTasksLogic(self)
        self.refresh_task_combo()

    def refresh_task_combo(self):
        """
        Clears and re-populates the select_task_combo from tasks_dreambot.json
        based on the 'task_name' key.
        """
        self.select_task_combo.clear()
        from appdata.logic.dreambot_tasks import load_tasks_dreambot
        tasks = load_tasks_dreambot()
        for t in tasks:
            if "task_name" in t:
                self.select_task_combo.addItem(t["task_name"])

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center()
