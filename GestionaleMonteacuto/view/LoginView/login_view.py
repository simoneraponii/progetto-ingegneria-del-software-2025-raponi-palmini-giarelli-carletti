from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

from app import session
from view.LoginView import resources_rc
from view.AgentView.AgentDashboard import AgentDashboardWindow

from controller.login_controller import LoginController
from model.enum.login_response import LoginResponse
from model.enum.ruolo import Ruolo
from app.session import Session
from view.UfficiomatricoleView.UfficioLogin import MainWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.session = Session()
        self.loginController = LoginController()
        self.dashboard = None

        self.setWindowTitle("Login")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: lightgray;")

        self.init_ui()

    # ---------------- UI ---------------- #

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Logo
        logo = QLabel()
        logo.setPixmap(
            QPixmap(":/Images/logo.png")
            .scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titolo
        title = QLabel("Ancona Montacuto\nCasa circondariale")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0056b3;")

        subtitle = QLabel("Inserisci le tue credenziali:")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setContentsMargins(0, 30, 0, 20)

        # Username
        lbl_username = QLabel("Username")
        self.username_txt = QLineEdit()
        self.username_txt.setPlaceholderText("Inserisci il tuo username")

        # Password
        lbl_password = QLabel("Password")
        self.password_txt = QLineEdit()
        self.password_txt.setPlaceholderText("Inserisci la tua password")
        self.password_txt.setEchoMode(QLineEdit.EchoMode.Password)

        for field in (self.username_txt, self.password_txt):
            field.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #aaa;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)

        # Buttons
        btn_login = QPushButton("ACCEDI")
        btn_info = QPushButton("INFO")

        btn_login.clicked.connect(self.handle_login)
        btn_info.clicked.connect(self.open_info_link)

        for btn in (btn_login, btn_info):
            btn.setFixedSize(140, 45)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    font-weight: bold;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_login)
        btn_layout.addSpacing(20)
        btn_layout.addWidget(btn_info)
        btn_layout.addStretch()

        # Layout composition
        main_layout.addWidget(logo)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(lbl_username)
        main_layout.addWidget(self.username_txt)
        main_layout.addWidget(lbl_password)
        main_layout.addWidget(self.password_txt)
        main_layout.addLayout(btn_layout)

    # ---------------- LOGIN ---------------- #

    def handle_login(self):
        username = self.username_txt.text().strip()
        password = self.password_txt.text().strip()

        result = self.loginController.login(username, password)

        if result.risposta == LoginResponse.OK:
            self.session.login(result.utente)

            if result.utente.ruolo == 'AGENTE':
                self.dashboard = AgentDashboardWindow(self.session)
                self.dashboard.show()
                self.hide()
            if result.utente.ruolo == 'UFFICIO_MATRICOLE':
                self.dashboard = MainWindow(self.session)
                self.dashboard.show()
                self.hide()

        elif result.risposta == LoginResponse.JUST_BLOCKED:
            QMessageBox.warning(
                self,
                "Account bloccato",
                "Il tuo account è stato temporaneamente bloccato.\n"
                "Riprova più tardi o contatta l'amministratore."
            )
            self.password_txt.clear()

        elif result.risposta == LoginResponse.ACCOUNT_BLOCKED:
            QMessageBox.critical(
                self,
                "Account bloccato",
                "Il tuo account è bloccato.\n"
                "Contatta l'amministratore."
            )
            self.password_txt.clear()
            self.username_txt.clear()

        elif result.risposta == LoginResponse.WRONG_PASSWORD:
            QMessageBox.warning(
                self,
                "Password errata",
                "La password inserita non è corretta."
            )
            self.password_txt.clear()

        elif result.risposta == LoginResponse.USER_NOT_FOUND:
            QMessageBox.warning(
                self,
                "Utente non trovato",
                "L'username inserito non esiste."
            )
            self.username_txt.clear()
            self.password_txt.clear()


    # ---------------- INFO ---------------- #

    def open_info_link(self):
        QDesktopServices.openUrl(
            QUrl("https://www.giustizia.it/giustizia/it/dettaglio_scheda.page?s=MII158941")
        )
