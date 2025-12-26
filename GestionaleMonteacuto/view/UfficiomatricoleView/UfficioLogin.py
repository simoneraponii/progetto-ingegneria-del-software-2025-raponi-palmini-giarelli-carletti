import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
from app.session import Session

class MainWindow(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        
        # Impostazione nome utente dinamico
        self.user_display_name = "Utente Sconosciuto"
        if self.session.current_user:
            user = self.session.current_user
            self.user_display_name = f"{user.nome} {user.cognome}"

        self.setWindowTitle("Ufficio Matricole - Home")
        self.setGeometry(200, 100, 1100, 650)
        self.setStyleSheet("background-color: black;")

        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -------------------------
        # BARRA SUPERIORE
        # -------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #e6e6e6;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        # Icona e Nome
        user_container = QWidget()
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(0,0,0,0)
        
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Arial", 20))
        
        name_label = QLabel(self.user_display_name)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #333;")
        
        user_layout.addWidget(user_icon)
        user_layout.addWidget(name_label)
        top_layout.addWidget(user_container, alignment=Qt.AlignmentFlag.AlignLeft)

        # Titolo centrale
        top_layout.addStretch()
        title = QLabel("Benvenuto Ufficio Matricole")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #555;")
        top_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        top_layout.addStretch()

        # Logout
        logout_btn = QPushButton(" Logout")
        logout_btn.setFixedSize(110, 40)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #bbb;
                border-radius: 10px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover { background-color: #ffdddd; border-color: red; }
        """)
        logout_btn.clicked.connect(self.handle_logout)
        top_layout.addWidget(logout_btn)

        main_layout.addWidget(top_bar)

        # -------------------------
        # SFONDO CENTRALE
        # -------------------------
        central_frame = QFrame()
        central_frame.setStyleSheet("background-color: #c1c1c1;")
        central_layout = QVBoxLayout(central_frame)
        
        # CARD CENTRALE
        card = QFrame()
        card.setFixedSize(400, 300)
        card.setStyleSheet("background-color: white; border-radius: 30px;")
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(25)

        utenti_btn = QPushButton("Gestisci Utenti")
        utenti_btn.setFixedHeight(50)
        utenti_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        utenti_btn.setStyleSheet("""
            QPushButton { 
                background-color: black; 
                color: white; 
                border-radius: 25px; 
                font-size: 16px; 
                font-weight: bold; 
            }
            QPushButton:hover { background-color: #333; }
        """)
        utenti_btn.clicked.connect(self.apri_visualizza_utenti)

        detenuti_btn = QPushButton("Gestisci Detenuti")
        detenuti_btn.setFixedHeight(50)
        detenuti_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        detenuti_btn.setStyleSheet("""
            QPushButton { background-color: #dedede; color: black; border-radius: 25px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #cecece; }
        """)
        # CORREZIONE: Senza parentesi per collegare il metodo
        detenuti_btn.clicked.connect(self.apri_visualizza_detenuti)

        card_layout.addWidget(utenti_btn)
        card_layout.addWidget(detenuti_btn)

        central_layout.addStretch()
        central_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        central_layout.addStretch()

        # LOGO BASSO DESTRA
        logo_row = QHBoxLayout()
        logo_row.addStretch()
        logo_label = QLabel()
        pix = QPixmap("logo.png") # Assicurati che il file esista o usa le risorse
        if not pix.isNull():
            logo_label.setPixmap(pix.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_row.addWidget(logo_label)
        central_layout.addLayout(logo_row)

        main_layout.addWidget(central_frame)

    def apri_visualizza_detenuti(self):
        """Metodo per aprire la finestra di gestione detenuti"""
        try:
            from view.UfficiomatricoleView.VisualizzaDetenuti import VisualizzaDetenuti
            self.detenuti_window = VisualizzaDetenuti(self.session)
            self.detenuti_window.show()
            # Se vuoi nascondere questa finestra quando apri l'altra:
            self.hide() 
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nel caricamento della vista:\n{e}")

    def apri_visualizza_utenti(self):
        """Metodo per aprire la finestra di gestione utenti"""
        try:
            from view.UfficiomatricoleView.VisualizzaUtenti import VisualizzaUtenti
            self.utenti_window = VisualizzaUtenti(self.session)
            self.utenti_window.show()
            self.hide()
        except Exception as e:
            self.show_message(
                "Errore",
                f"Errore nel caricamento della vista utenti:\n{e}",
                QMessageBox.Icon.Critical
            )



    def handle_logout(self):
        confirm = QMessageBox.question(self, "Logout", "Vuoi uscire?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.session.current_user = None
            self.close()
            from view.LoginView.login_view import LoginWindow
            self.login = LoginWindow()
            self.login.show()

    def show_message(self, title, text, icon=QMessageBox.Icon.Information, buttons=QMessageBox.StandardButton.Ok):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(buttons)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #e6e6e6;
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 6px 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #d6d6d6;
            }
        """)

        return msg.exec()

