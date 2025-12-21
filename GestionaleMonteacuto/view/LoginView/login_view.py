from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from view.LoginView import resources_rc

from view.AgentView.AgentDashboard import AgentDashboardWindow

from controller.login_controller import LoginController
from model.user.login_result import LoginResult
from model.enum.login_response import LoginResponse
from app.session import Session
from model.enum.ruolo import Ruolo

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setWindowTitle("Login")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: light gray;")
        self.init_login_ui()
        self.loginController = LoginController()
        self.session = Session()
        

    def init_login_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)

        # Logo
        logo = QLabel()
        logo.setPixmap(QPixmap(":/Images/logo.png").scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titolo
        title = QLabel("Ancona Montacuto\nCasa circondariale")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0056b3;")

        subtitle = QLabel("Inserisci le tue credenziali:")
        subtitle.setFont(QFont("Arial", 15))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignJustify)
        subtitle.setContentsMargins(0, 50, 0, 0)

        # Campi di input
        lbl_username = QLabel("Username")
        lbl_username.setFont(QFont("Arial", 10))
        lbl_username.setStyleSheet("color: gray;")

        self.username_txt = QLineEdit()
        self.username_txt.setPlaceholderText("Inserisci il tuo username")

        lbl_password = QLabel("Password")
        lbl_password.setFont(QFont("Arial", 10))
        lbl_password.setStyleSheet("color: gray;")

        self.password_txt = QLineEdit()
        self.password_txt.setPlaceholderText("Inserisci la tua password")
        self.password_txt.setEchoMode(QLineEdit.EchoMode.Password)

        for field in [self.username_txt, self.password_txt]:
            field.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #aaa;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)

        # Bottoni Accedi e Info
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 20, 0, 0)
        btn_layout.setSpacing(300)  
        btn_login = QPushButton("ACCEDI")
        btn_login.setFixedSize(140, 50)  
        btn_info = QPushButton("INFO")
        btn_info.setFixedSize(140, 50)
        btn_info.clicked.connect(self.apri_link)

        btn_login.clicked.connect(self.handle_login)

        for btn in [btn_login, btn_info]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedWidth(100)

        # Sistemazione del layout
        btn_layout.addStretch()
        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_info)
        btn_layout.addStretch()

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        user_layout = QVBoxLayout()
        user_layout.setSpacing(2)
        user_layout.addWidget(lbl_username)
        user_layout.addWidget(self.username_txt)
        layout.addLayout(user_layout)

        pass_layout = QVBoxLayout()
        pass_layout.setSpacing(2)
        pass_layout.addWidget(lbl_username)
        pass_layout.addWidget(self.password_txt)
        layout.addLayout(pass_layout)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    # Metodo per il login
    def handle_login(self):
        result = self.loginController.login(self.username_txt.text().strip(), self.password_txt.text().strip())
        
        if result.risposta == LoginResponse.OK:
            self.session.login(result.utente)
            if result.utente.ruolo == Ruolo.AGENTE:
                dashboard = AgentDashboardWindow(self.session)
                dashboard.show()
                self.close()

        # elif result.risposta == LoginResponse.ACCOUNT_BLOCKED:
        #     QMessageBox.warning(self, "Account bloccato", "Il tuo account è bloccato. Contatta l'amministratore.")
        #     # self.password_txt.clear()
        #     # self.username_txt.clear()
        # elif result.risposta == LoginResponse.WRONG_PASSWORD:
        #     QMessageBox.warning(self, "Password errata", "La password inserita non è corretta. Riprova.")
        #     self.password_txt.clear()
        # elif result.risposta == LoginResponse.USER_NOT_FOUND:
        #     QMessageBox.warning(self, "Utente non trovato", "L'username inserito non esiste. Riprova.")
        #     self.password_txt.clear()
        #     self.username_txt.clear()
    
    
        

    # Metodo per bottone info   
    def apri_link(self):
        QDesktopServices.openUrl(QUrl("https://www.giustizia.it/giustizia/it/dettaglio_scheda.page?s=MII158941"))


app = QApplication([])
window = LoginWindow()
window.show()
app.exec()