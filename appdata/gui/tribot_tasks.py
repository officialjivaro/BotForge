# \appdata\gui\tribot_tasks.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QCheckBox
)
from appdata.logic.tribot_tasks import TRiBotTasksLogic

class TRiBotTasksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRiBot Task Manager")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        form_layout = QFormLayout()

        self.task_name_input = QLineEdit()
        form_layout.addRow("Task Name:", self.task_name_input)

        self.script_id_input = QLineEdit()
        form_layout.addRow("Script Name:", self.script_id_input)

        self.args_input = QLineEdit()
        form_layout.addRow("Args/Params:", self.args_input)

        main_layout.addLayout(form_layout)

        radio_layout = QHBoxLayout()
        self.run_until_stopped_radio = QRadioButton("Run Script until Stopped")
        self.run_for_radio = QRadioButton("Run For:")
        radio_layout.addWidget(self.run_until_stopped_radio)
        radio_layout.addWidget(self.run_for_radio)
        main_layout.addLayout(radio_layout)

        run_for_layout = QFormLayout()
        self.run_from_input = QLineEdit()
        self.run_to_input = QLineEdit()
        run_for_layout.addRow("Run From (mins):", self.run_from_input)
        run_for_layout.addRow("To (mins):", self.run_to_input)
        main_layout.addLayout(run_for_layout)

        loop_layout = QHBoxLayout()
        self.loop_checkbox = QCheckBox("Loop")
        loop_layout.addWidget(self.loop_checkbox)
        main_layout.addLayout(loop_layout)

        break_for_layout = QFormLayout()
        self.break_from_input = QLineEdit()
        self.break_to_input = QLineEdit()
        break_for_layout.addRow("Break From (mins):", self.break_from_input)
        break_for_layout.addRow("To (mins):", self.break_to_input)
        main_layout.addLayout(break_for_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # Instantiate the TRiBotTasksLogic helper class
        self.logic = TRiBotTasksLogic(self)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center()
