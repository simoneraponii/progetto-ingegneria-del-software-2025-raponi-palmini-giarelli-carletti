import sys
import os
import logging
import ctypes
import platform
import threading
import time
import traceback
import signal
from PyQt6.QtWidgets import QApplication

from view.LoginView.login_view import LoginWindow
from app.session import Session

from view.UfficiomatricoleView.UfficioLogin import MainWindow


def gestionale():
    app = QApplication(sys.argv)

    session = Session()
    login = LoginWindow()
    login.show()

    sys.exit(app.exec())



if __name__  ==  "__main__":
    gestionale()