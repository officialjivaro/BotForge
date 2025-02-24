# \appdata\logic\main_page.py

import os
import threading
import urllib.request
import webbrowser
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal, QTimer

from appdata.gui.account_manager import AccountsPage
from appdata.gui.dreambot_tasks import DreamBotTasksWindow
from appdata.gui.osbot_tasks import OsbotTasksWindow
from appdata.gui.tribot_tasks import TRiBotTasksWindow
from appdata.gui.proxy_manager import ProxyManager
from appdata.gui.general_settings import GeneralSettingsWindow
from appdata.message_box.download_complete import DownloadCompleteWindow

class MainDispatcher(QObject):
    downloadFinished = Signal()
    downloadError = Signal(str)

main_dispatcher = MainDispatcher()

accounts_window = None
dreambot_manager_window = None
download_complete_window = None
osbot_manager_window = None
osbot_tasks_window = None
proxy_manager_window = None
tribot_manager_window = None
general_settings_window = None

def show_download_complete():
    global download_complete_window
    download_complete_window = DownloadCompleteWindow()
    download_complete_window.exec()

def show_download_error(msg):
    QMessageBox.critical(None, "Download Error", msg)

main_dispatcher.downloadFinished.connect(show_download_complete)
main_dispatcher.downloadError.connect(show_download_error)

def open_buy_proxies():
    url = "https://jivaro.net/content/blog/the-best-affordable-proxy-providers"
    webbrowser.open(url)

def open_visit_website():
    url = "https://jivaro.net/"
    webbrowser.open(url)

def open_botting_guide():
    url = "https://jivaro.net/content/guides/the-ultimate-guide-to-botting-old-school-runescape"
    webbrowser.open(url)

def open_accounts_page():
    global accounts_window
    accounts_window = AccountsPage()
    accounts_window.show()

def open_create_osrs_account():
    url = "https://secure.runescape.com/m=account-creation/create_account"
    webbrowser.open(url)

def open_tribot_manager():
    global tribot_manager_window
    from appdata.gui.tribot_manager import TribotManager
    tribot_manager_window = TribotManager()
    tribot_manager_window.show()

def open_dreambot_manager():
    global dreambot_manager_window
    from appdata.gui.dreambot_manager import DreambotManager
    dreambot_manager_window = DreambotManager()
    dreambot_manager_window.show()

def open_osbot_manager():
    global osbot_manager_window
    from appdata.gui.osbot_manager import OsbotManager
    osbot_manager_window = OsbotManager()
    osbot_manager_window.show()

def open_dreambot_tasks():
    global dreambot_tasks_window
    dreambot_tasks_window = DreamBotTasksWindow()
    dreambot_tasks_window.show()

def open_osbot_tasks():
    global osbot_tasks_window
    osbot_tasks_window = OsbotTasksWindow()
    osbot_tasks_window.show()

def open_tribot_tasks():
    global tribot_tasks_window
    tribot_tasks_window = TRiBotTasksWindow()
    tribot_tasks_window.show()

def open_proxy_manager():
    global proxy_manager_window
    proxy_manager_window = ProxyManager()
    proxy_manager_window.show()

def open_general_settings():
    global general_settings_window
    general_settings_window = GeneralSettingsWindow()
    general_settings_window.show()

def download_osbot():
    def worker():
        try:
            url = "http://osbot.org/mvc/get"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            response = urllib.request.urlopen(req)
            data = response.read()

            try:
                username = os.getlogin()
            except:
                username = os.environ.get("USERNAME", "default")
            dest_dir = os.path.join("C:\\Users", username, "Jivaro", "BotForge", "Data", "Clients")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, "OSBot.jar")
            with open(dest_path, "wb") as f:
                f.write(data)

            main_dispatcher.downloadFinished.emit()
        except Exception as e:
            main_dispatcher.downloadError.emit(str(e))

    t = threading.Thread(target=worker)
    t.start()

def download_dreambot():
    def worker():
        try:
            url = "https://downloads.dreambot.org/DBLauncher.jar"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            response = urllib.request.urlopen(req)
            data = response.read()

            try:
                username = os.getlogin()
            except:
                username = os.environ.get("USERNAME", "default")
            dest_dir = os.path.join("C:\\Users", username, "Jivaro", "BotForge", "Data", "Clients")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, "DreamBot.jar")
            with open(dest_path, "wb") as f:
                f.write(data)

            main_dispatcher.downloadFinished.emit()
        except Exception as e:
            main_dispatcher.downloadError.emit(str(e))

    t = threading.Thread(target=worker)
    t.start()

def download_tribot():
    def worker():
        try:
            url = "https://installers.tribot.org/tribot-splash.jar"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            response = urllib.request.urlopen(req)
            data = response.read()

            try:
                username = os.getlogin()
            except:
                username = os.environ.get("USERNAME", "default")
            dest_dir = os.path.join("C:\\Users", username, "Jivaro", "BotForge", "Data", "Clients")
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, "TRiBot.jar")
            with open(dest_path, "wb") as f:
                f.write(data)

            main_dispatcher.downloadFinished.emit()
        except Exception as e:
            main_dispatcher.downloadError.emit(str(e))

    t = threading.Thread(target=worker)
    t.start()
