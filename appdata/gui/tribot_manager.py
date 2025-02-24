# \appdata\gui\tribot_manager.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel
from appdata.logic.datagridview_populate import populate_datagridview
from appdata.logic.tribot_manager import TRiBotManagerLogic

class TribotManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRiBot Manager")
        
        self.column_ratios = [25, 20, 20, 10, 15, 10]
        self.init_ui()
        self.logic = TRiBotManagerLogic(self)

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.table_view = QTableView()
        self.model = QStandardItemModel(0, 6, self)
        self.model.setHorizontalHeaderLabels(["Account", "Proxy", "Task", "World", "Notes", "Status"])
        self.table_view.setModel(self.model)
        
        self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setMinimumWidth(600)

        header = self.table_view.horizontalHeader()
        for col in range(self.model.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Interactive)
        
        layout.addWidget(self.table_view)
        
        populate_datagridview(self.model, task_key="tribot_task")

        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run")
        self.stop_button = QPushButton("Stop")
        self.edit_button = QPushButton("Edit")
        self.cli_settings_button = QPushButton("CLI Settings")
        
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.cli_settings_button)
        
        layout.addLayout(button_layout)
    
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def showEvent(self, event):
        super().showEvent(event)
        self.center()
        self.resize_columns()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_columns()

    def resize_columns(self):
        total_width = self.table_view.viewport().width()
        total_ratio = sum(self.column_ratios)
        header = self.table_view.horizontalHeader()
        for col, ratio in enumerate(self.column_ratios):
            col_width = int(total_width * (ratio / total_ratio))
            header.resizeSection(col, col_width)
