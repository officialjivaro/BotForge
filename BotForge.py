# \BotForge.py

import sys
from PySide6.QtWidgets import QApplication
from appdata.gui.main_page import MainPage

def main():
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
