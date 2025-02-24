# \appdata\gui\dreambot_cli_settings.py

import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator

def get_cli_settings_path():
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USERNAME", "default")
    return f"C:\\Users\\{username}\\Jivaro\\BotForge\\Data\\cli_settings.json"

def load_cli_settings():
    path = get_cli_settings_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_cli_settings(data_list):
    path = get_cli_settings_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2)

class DreamBotCLISettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DreamBot CLI Settings")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        form_layout = QFormLayout()

        self.break_nickname_input = QLineEdit()
        form_layout.addRow("Break Nickname:", self.break_nickname_input)

        self.covert_mode_checkbox = QCheckBox("Covert Mode")
        form_layout.addRow(self.covert_mode_checkbox)

        self.fps_input = QLineEdit()
        self.fps_input.setValidator(QIntValidator(1, 50))
        form_layout.addRow("FPS (1-50):", self.fps_input)

        self.fresh_start_checkbox = QCheckBox("Fresh Start")
        form_layout.addRow(self.fresh_start_checkbox)

        self.layout_combo = QComboBox()
        self.layout_combo.addItems(["fixed", "resizable_classic", "resizable_modern"])
        form_layout.addRow("Layout:", self.layout_combo)

        self.mouse_speed_input = QLineEdit()
        self.mouse_speed_input.setValidator(QIntValidator(1, 100))
        form_layout.addRow("Mouse Speed (1-100):", self.mouse_speed_input)

        self.render_combo = QComboBox()
        self.render_combo.addItems(["all", "script", "none"])
        form_layout.addRow("Render:", self.render_combo)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.save_button.clicked.connect(self.handle_save)
        self.cancel_button.clicked.connect(self.handle_cancel)

    def populate_fields(self):
        """
        Loads any existing DreamBot CLI settings from the JSON file
        and populates the controls if an object with client="dreambot" is found.
        """
        data_list = load_cli_settings()
        dreambot_obj = None
        for obj in data_list:
            if obj.get("client") == "dreambot":
                dreambot_obj = obj
                break

        if dreambot_obj:
            self.break_nickname_input.setText(dreambot_obj.get("break_nickname", ""))
            self.covert_mode_checkbox.setChecked(bool(dreambot_obj.get("covert_mode", False)))
            self.fps_input.setText(str(dreambot_obj.get("fps", 25)))
            self.fresh_start_checkbox.setChecked(bool(dreambot_obj.get("fresh_start", False)))
            layout_val = dreambot_obj.get("layout", "fixed")
            if layout_val in ["fixed", "resizable_classic", "resizable_modern"]:
                idx = self.layout_combo.findText(layout_val)
                if idx != -1:
                    self.layout_combo.setCurrentIndex(idx)
            self.mouse_speed_input.setText(str(dreambot_obj.get("mouse_speed", 15)))
            render_val = dreambot_obj.get("render", "all")
            if render_val in ["all", "script", "none"]:
                idx = self.render_combo.findText(render_val)
                if idx != -1:
                    self.render_combo.setCurrentIndex(idx)

    def handle_save(self):
        break_nickname = self.break_nickname_input.text().strip()
        covert_mode = self.covert_mode_checkbox.isChecked()
        fps_str = self.fps_input.text().strip()
        fresh_start = self.fresh_start_checkbox.isChecked()
        layout_val = self.layout_combo.currentText()
        mouse_speed_str = self.mouse_speed_input.text().strip()
        render_val = self.render_combo.currentText()

        if not fps_str:
            QMessageBox.warning(self, "Invalid FPS", "Please enter a valid FPS (1-50).")
            return
        if not mouse_speed_str:
            QMessageBox.warning(self, "Invalid Mouse Speed", "Please enter a valid Mouse Speed (1-100).")
            return

        try:
            fps_val = int(fps_str)
            mouse_speed_val = int(mouse_speed_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "FPS and Mouse Speed must be integers.")
            return

        data_list = load_cli_settings()
        # Remove any existing DreamBot object
        data_list = [obj for obj in data_list if obj.get("client") != "dreambot"]

        new_obj = {
            "client": "dreambot",
            "break_nickname": break_nickname,
            "covert_mode": covert_mode,
            "fps": fps_val,
            "fresh_start": fresh_start,
            "layout": layout_val,
            "mouse_speed": mouse_speed_val,
            "render": render_val
        }
        data_list.append(new_obj)
        save_cli_settings(data_list)

        QMessageBox.information(self, "Saved", "DreamBot CLI Settings saved successfully.")

    def handle_cancel(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
        # Populate the fields from the JSON whenever the window is shown
        self.populate_fields()
