# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QScrollArea,
    QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt

# --- IMPORT ---
# Assicurati che il file resources_rc sia generato o accessibile
try:
    from view.AgentView import resources_rc
except ImportError:
    pass # Gestione caso senza risorse compilate

from controller.account_controller import AccountController
from model.DTO.user_dto import UserDTO
from app.session import Session

class VisualizzaUtenti(QWidget):
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)

        self.session = session
        self.controller = AccountController()

        # Nome utente formattato per la barra in alto
        self.operatore_nome = f"{session.current_user.ruolo} {session.current_user.cognome}"

        self.setWindowTitle("Gestione Utenti")
        self.setGeometry(100, 100, 1200, 700)
        
        # SFONDO GENERALE (Nero come richiesto)
        self.setStyleSheet("background-color: black;")

        # Caricamento dati iniziali
        self.utenti = self.load_utenti()

        self.init_ui()

    # ==========================================
    # LOGICA DATI
    # ==========================================
    def load_utenti(self) -> list[UserDTO]:
        try:
            utenti = self.controller.get_utenti_dto()
            # Ordina per Cognome e poi Nome
            return sorted(
                utenti,
                key=lambda u: (u.cognome.lower(), u.nome.lower())
            )
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare gli utenti:\n{e}")
            return []

    # ==========================================
    # INTERFACCIA UTENTE
    # ==========================================
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --------------------------------------
        # BARRA SUPERIORE (Grigio Chiaro)
        # --------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #e6e6e6;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        # SINISTRA: Indietro + Icona + Nome
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        back_btn = QPushButton()
        back_btn.setIcon(QIcon(":/Images/Images/back.png")) 
        back_btn.setFixedSize(45, 45)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #bbb;
                border-radius: 22px;
            }
            QPushButton:hover { background-color: #f0f0f0; border-color: #3498db; }
        """)
        back_btn.clicked.connect(self.vai_indietro)

        user_icon = QLabel()
        # Usa un'icona generica o specifica se ce l'hai
        user_icon.setPixmap(QPixmap(":/Images/Images/agente.png").scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio))
        
        name_label = QLabel(self.operatore_nome)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #333;")

        left_layout.addWidget(back_btn)
        left_layout.addWidget(user_icon)
        left_layout.addWidget(name_label)
        
        # CENTRO: Titolo
        title_label = QLabel("Amministrazione Utenti")
        title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #555;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DESTRA: Logout
        logout_btn = QPushButton(" Logout")
        logout_btn.setIcon(QIcon(":/Images/Images/logout.png"))
        logout_btn.setFixedSize(110, 40)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #bbb;
                border-radius: 10px;
                color: #333;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ffdddd; border-color: red; }
        """)
        logout_btn.clicked.connect(self.logout)

        top_layout.addWidget(left_container, stretch=1)
        top_layout.addWidget(title_label, stretch=2)
        top_layout.addWidget(logout_btn, stretch=1, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(top_bar)

        # --------------------------------------
        # AREA CENTRALE
        # --------------------------------------
        central_frame = QFrame()
        central_frame.setStyleSheet("background-color: #c1c1c1;") # Grigio medio come richiesto
        central_layout = QVBoxLayout(central_frame)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setSpacing(15)

        # Header: Titolo sezione + Nuovo Utente + Aggiorna Lista
        header_row = QHBoxLayout()
        section_title = QLabel("Elenco Staff")
        section_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #444;")

        # Pulsante Nuovo Utente
        btn_new = QPushButton("➕ Nuovo Utente")
        btn_new.setFixedSize(180, 45)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        btn_new.clicked.connect(self.nuovo_utente)

        # Pulsante Aggiorna Lista
        btn_refresh = QPushButton("🔄 Aggiorna")
        btn_refresh.setFixedSize(150, 45)
        btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #e67e22; }
        """)
        btn_refresh.clicked.connect(self.aggiorna_lista)

        header_row.addWidget(section_title)
        header_row.addStretch()
        header_row.addWidget(btn_new)
        header_row.addWidget(btn_refresh)
        central_layout.addLayout(header_row)

        # Search Bar
        search_frame = QFrame()
        search_frame.setFixedHeight(60)
        search_frame.setStyleSheet("background-color: white; border-radius: 20px;")
        search_layout = QHBoxLayout(search_frame)
        
        icon_lens = QLabel("🔍")
        icon_lens.setFont(QFont("Arial", 16))
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca per Cognome, Nome o Username...")
        self.search_bar.setFont(QFont("Arial", 14))
        self.search_bar.setStyleSheet("border: none; background: transparent;")
        self.search_bar.textChanged.connect(self.filter_list)
        
        search_layout.addWidget(icon_lens)
        search_layout.addWidget(self.search_bar)
        central_layout.addWidget(search_frame)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #c1c1c1;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)

        self.populate_list(self.utenti)

        self.scroll_area.setWidget(self.scroll_content)
        central_layout.addWidget(self.scroll_area)

        # Logo in basso
        logo_row = QHBoxLayout()
        logo_row.addStretch()
        logo_label = QLabel()
        logo_pix = QPixmap(":/Images/Images/logo.png")
        if not logo_pix.isNull():
            logo_label.setPixmap(logo_pix.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        logo_row.addWidget(logo_label)
        central_layout.addLayout(logo_row)

        main_layout.addWidget(central_frame)

    # ==========================================
    # LOGICA POPOLAMENTO
    # ==========================================
    def populate_list(self, data_list: list[UserDTO]):
        # Pulisce la lista attuale
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item.widget(): item.widget().deleteLater()

        if not data_list:
            lbl = QLabel("Nessun utente trovato.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 12))
            self.scroll_layout.addWidget(lbl)
            return

        for user in data_list:
            row_frame = QFrame()
            row_frame.setFixedHeight(75)
            row_frame.setStyleSheet("background-color: white; border-radius: 15px;")
            row_layout = QHBoxLayout(row_frame)

            # Stile campi sola lettura (finti input per estetica)
            input_style = "background: #f7f7f7; border: 1px solid #bbb; border-radius: 8px; padding: 5px; color: black;"

            # Cognome
            edt_cog = QLineEdit(user.cognome)
            edt_cog.setReadOnly(True)
            edt_cog.setPlaceholderText("Cognome")
            edt_cog.setStyleSheet(input_style)

            # Nome
            edt_nom = QLineEdit(user.nome)
            edt_nom.setReadOnly(True)
            edt_nom.setPlaceholderText("Nome")
            edt_nom.setStyleSheet(input_style)

            # Ruolo
            edt_ruolo = QLineEdit(user.ruolo.value if hasattr(user.ruolo, 'value') else str(user.ruolo))
            edt_ruolo.setReadOnly(True)
            edt_ruolo.setFixedWidth(150)
            edt_ruolo.setStyleSheet(input_style)

            # Stato (Badge Colorato)
            lbl_stato = QLabel("ATTIVO" if user.tentativi > 0 else "BLOCCATO")
            lbl_stato.setFixedWidth(100)
            lbl_stato.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Colori badge: Verde se attivo, Rosso se bloccato
            colore_bg = "#d4edda" if user.tentativi > 0 else "#f8d7da"
            colore_text = "#155724" if user.tentativi > 0 else "#721c24"
            
            lbl_stato.setStyleSheet(f"""
                background-color: {colore_bg};
                color: {colore_text};
                border-radius: 8px;
                font-weight: bold;
                padding: 5px;
            """)

            # PULSANTE MODIFICA
            btn_edit = QPushButton("Modifica")
            btn_edit.setFixedSize(100, 40)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                }
                QPushButton:hover { background-color: #2980b9; }
            """)
            btn_edit.clicked.connect(lambda checked, u=user.username: self.modifica_utente(u))

            # Aggiunta widget al layout orizzontale della riga
            row_layout.addWidget(edt_cog, stretch=2)
            row_layout.addWidget(edt_nom, stretch=2)
            row_layout.addWidget(edt_ruolo, stretch=1)
            row_layout.addWidget(lbl_stato)
            row_layout.addWidget(btn_edit)

            self.scroll_layout.addWidget(row_frame)
        
        self.scroll_layout.addStretch()

    # ==========================================
    # NAVIGAZIONE E AZIONI
    # ==========================================
    def filter_list(self):
        testo = self.search_bar.text().lower().strip()
        if not testo:
            self.populate_list(self.utenti)
            return
            
        filtrati = [
            u for u in self.utenti 
            if testo in u.cognome.lower() or testo in u.nome.lower() or testo in u.username.lower()
        ]
        self.populate_list(filtrati)

    def vai_indietro(self):
        # Sostituisci con la tua classe di menu principale/admin
        # from view.AdminView.AdminDashboard import AdminDashboard
        # self.back_win = AdminDashboard(self.session)
        # self.back_win.show()
        self.close()

    def nuovo_utente(self):
        try:
            from view.UfficiomatricoleView.NuovoUtenteView import NuovoUtenteView
            self.new_win = NuovoUtenteView(self.session)
            self.new_win.show()
        except ImportError as e:
            print(f"Errore di import: {e}")
            QMessageBox.critical(self, "Errore", f"Impossibile caricare la vista: {e}")

    def modifica_utente(self, username: str):
        from view.UfficiomatricoleView.EditUtenteView import EditUtenteView
        self.view_win = EditUtenteView(self.session, username)
        self.view_win.show()

    def logout(self):
        if QMessageBox.question(self, "Logout", "Uscire dal sistema?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.session.current_user = None
            from view.LoginView.login_view import LoginWindow
            self.login_win = LoginWindow()
            self.login_win.show()
            self.close()

    def aggiorna_lista(self):
        try:
            self.utenti = self.load_utenti()
            self.populate_list(self.utenti)
            # Resetta ricerca
            self.search_bar.clear()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile aggiornare la lista:\n{e}")