# \appdata\gui\osbot_manager.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QAbstractItemView, QHeaderView
)
from PySide6.QtGui import QStandardItemModel

class OsbotManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSBot Manager")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create a table view (datagridview-like control)
        self.table_view = QTableView()
        self.model = QStandardItemModel(0, 6, self)
        self.model.setHorizontalHeaderLabels(["Account", "Proxy", "Task", "World", "Notes", "Status"])
        self.table_view.setModel(self.model)
        
        # Enable extended selection (multiple selection using Shift/Ctrl)
        self.table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Set a minimum width so that all headers are visible
        self.table_view.setMinimumWidth(600)
        
        # Ensure headers expand with the table view's width
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.table_view)
        
        # Bottom button layout with Run, Stop, Edit, and CLI Settings buttons
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