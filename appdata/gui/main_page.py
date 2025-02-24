# \appdata\gui\main_page.py

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMenuBar, QMenu
)
from PySide6.QtGui import QAction, QPalette, QColor
from appdata.logic.main_page import (
    open_buy_proxies,
    open_visit_website,
    open_botting_guide,
    open_accounts_page,
    open_create_osrs_account,
    open_tribot_manager,
    open_dreambot_manager,
    open_osbot_manager,
    open_proxy_manager,
    download_osbot,
    open_tribot_tasks,
    open_dreambot_tasks,
    open_osbot_tasks,
    download_dreambot,
    download_tribot,
    open_general_settings
)

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotForge v0.01")

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        accounts_action = QAction("Accounts", self)
        proxy_settings_action = QAction("Proxy Settings", self)
        general_settings_action = QAction("General Settings", self)
        file_menu.addAction(accounts_action)
        file_menu.addAction(proxy_settings_action)
        file_menu.addAction(general_settings_action)
        accounts_action.triggered.connect(open_accounts_page)
        proxy_settings_action.triggered.connect(open_proxy_manager)
        general_settings_action.triggered.connect(open_general_settings)

        tasks_menu = menu_bar.addMenu("Tasks")
        tribot_task_action = QAction("TRiBot", self)
        dreambot_task_action = QAction("DreamBot", self)
        osbot_task_action = QAction("OSBot", self)
        tasks_menu.addAction(tribot_task_action)
        tasks_menu.addAction(dreambot_task_action)
        tasks_menu.addAction(osbot_task_action)
        tribot_task_action.triggered.connect(open_tribot_tasks)
        dreambot_task_action.triggered.connect(open_dreambot_tasks)
        osbot_task_action.triggered.connect(open_osbot_tasks)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        dashboard_label = QLabel("Client Dashboard")
        main_layout.addWidget(dashboard_label)

        dashboard_layout = QHBoxLayout()
        tribot_button = QPushButton("TRiBot")
        dreambot_button = QPushButton("DreamBot")
        osbot_button = QPushButton("OSBot")
        dashboard_layout.addWidget(tribot_button)
        dashboard_layout.addWidget(dreambot_button)
        dashboard_layout.addWidget(osbot_button)
        main_layout.addLayout(dashboard_layout)

        tribot_button.clicked.connect(open_tribot_manager)
        dreambot_button.clicked.connect(open_dreambot_manager)
        osbot_button.clicked.connect(open_osbot_manager)

        download_label = QLabel("Client Download")
        main_layout.addWidget(download_label)

        download_layout = QHBoxLayout()
        tribot_dl_button = QPushButton("TriBot")
        dreambot_dl_button = QPushButton("DreamBot")
        osbot_dl_button = QPushButton("OSBot")
        download_layout.addWidget(tribot_dl_button)
        download_layout.addWidget(dreambot_dl_button)
        download_layout.addWidget(osbot_dl_button)
        main_layout.addLayout(download_layout)

        tribot_dl_button.clicked.connect(download_tribot)
        dreambot_dl_button.clicked.connect(download_dreambot)
        osbot_dl_button.clicked.connect(download_osbot)

        misc_label = QLabel("Miscellaneous")
        main_layout.addWidget(misc_label)

        misc_layout_row1 = QHBoxLayout()
        script_factory_button = QPushButton("Download Script Factory Scripts")
        java_button = QPushButton("Download Java")
        buy_proxies_button = QPushButton("Buy Proxies")
        misc_layout_row1.addWidget(script_factory_button)
        misc_layout_row1.addWidget(java_button)
        misc_layout_row1.addWidget(buy_proxies_button)
        main_layout.addLayout(misc_layout_row1)

        misc_layout_row2 = QHBoxLayout()
        create_account_button = QPushButton("Create OSRS Account")
        botting_guide_button = QPushButton("Botting Guide")
        visit_website_button = QPushButton("Visit Website")
        misc_layout_row2.addWidget(create_account_button)
        misc_layout_row2.addWidget(botting_guide_button)
        misc_layout_row2.addWidget(visit_website_button)
        main_layout.addLayout(misc_layout_row2)

        buy_proxies_button.clicked.connect(open_buy_proxies)
        botting_guide_button.clicked.connect(open_botting_guide)
        visit_website_button.clicked.connect(open_visit_website)
        create_account_button.clicked.connect(open_create_osrs_account)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(44, 44, 44))
        palette.setColor(QPalette.WindowText, QColor(236, 236, 236))
        palette.setColor(QPalette.Base, QColor(64, 64, 64))
        palette.setColor(QPalette.AlternateBase, QColor(80, 80, 80))
        palette.setColor(QPalette.ToolTipBase, QColor(236, 236, 236))
        palette.setColor(QPalette.ToolTipText, QColor(44, 44, 44))
        palette.setColor(QPalette.Text, QColor(236, 236, 236))
        palette.setColor(QPalette.Button, QColor(64, 64, 64))
        palette.setColor(QPalette.ButtonText, QColor(236, 236, 236))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(100, 100, 100))
        palette.setColor(QPalette.HighlightedText, QColor(236, 236, 236))
        self.setPalette(palette)

        self.setStyleSheet("""
            QLabel {
                color: #ececec;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ececec;
                padding: 5px;
                margin: 2px;
            }
            QMenuBar {
                background-color: #2c2c2c;
                color: #ececec;
            }
            QMenu {
                background-color: #2c2c2c;
                color: #ececec;
            }
        """)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        super().showEvent(event)
        self.center()
