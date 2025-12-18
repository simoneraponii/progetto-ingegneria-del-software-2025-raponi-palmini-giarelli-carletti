from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from View.LoginView import resources_rc
import sys
from View.AgentView.AgentDashboard import AgentDashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setWindowTitle("Login")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: light gray;")
        self.init_login_ui()

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
        username_label = QLabel("Username")
        username_label.setFont(QFont("Arial", 10))
        username_label.setStyleSheet("color: gray;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Inserisci il tuo username")

        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 10))
        password_label.setStyleSheet("color: gray;")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Inserisci la tua password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        for field in [self.username, self.password]:
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
        login_btn = QPushButton("ACCEDI")
        login_btn.setFixedSize(140, 50)  
        info_btn = QPushButton("INFO")
        info_btn.setFixedSize(140, 50)
        info_btn.clicked.connect(self.apri_link)

        login_btn.clicked.connect(self.handle_login)

        for btn in [login_btn, info_btn]:
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
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(info_btn)
        btn_layout.addStretch()

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        user_layout = QVBoxLayout()
        user_layout.setSpacing(2)
        user_layout.addWidget(username_label)
        user_layout.addWidget(self.username)
        layout.addLayout(user_layout)

        pass_layout = QVBoxLayout()
        pass_layout.setSpacing(2)
        pass_layout.addWidget(password_label)
        pass_layout.addWidget(self.password)
        layout.addLayout(pass_layout)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    # Metodo per il login
    def handle_login(self):
        agente_nome = self.username.text()
        dashboard = AgentDashboardWindow(agente_nome)
        dashboard.show()
        self.close()
    
    # Metodo per bottone info   
    def apri_link(self):
        QDesktopServices.openUrl(QUrl("https://www.giustizia.it/giustizia/it/dettaglio_scheda.page?s=MII158941"))

app = QApplication([])
window = LoginWindow()
window.show()
app.exec()
