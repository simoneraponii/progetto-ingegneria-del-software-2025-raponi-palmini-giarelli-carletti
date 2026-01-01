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
# Assicurati che questi import puntino ai tuoi file corretti
from view.AgentView import resources_rc
from controller.detenuti_controller import DetenutiController
from model.DTO.detenuto_dto import DetenutoDTO
from app.session import Session

class VisualizzaDetenuti(QWidget):
    def __init__(self, session: Session, parent=None):
        super().__init__() # Finestra indipendente
        
        self.session = session
        self.parent_window = parent # Riferimento alla finestra precedente
        self.detenuto_controller = DetenutiController()

        # Nome utente formattato
        self.operatore_nome = f"{session.current_user.ruolo} {session.current_user.cognome}"

        self.setWindowTitle("Dashboard Ufficio Matricole")
        self.setGeometry(100, 100, 1200, 700)
        
        # SFONDO GENERALE NERO (Questo causava il problema al popup)
        self.setStyleSheet("background-color: black;")

        # Caricamento dati iniziali
        self.detainees = self.load_detenuti()

        self.init_ui()

    # ==========================================
    # LOGICA DATI
    # ==========================================
    def load_detenuti(self) -> list[DetenutoDTO]:
        try:
            detenuti = self.detenuto_controller.getDetenutiDto()
            # Ordina per Cognome, poi Nome
            return sorted(
                detenuti,
                key=lambda d: (d.cognome.lower(), d.nome.lower(), d.matricola.lower())
            )
        except Exception as e:
            # Anche qui usiamo uno stile forzato per evitare illeggibilità
            err = QMessageBox(self)
            err.setWindowTitle("Errore")
            err.setText(f"Impossibile caricare i detenuti:\n{e}")
            err.setStyleSheet("background-color: white; color: black;")
            err.exec()
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
        user_icon.setPixmap(QPixmap(":/Images/Images/agente.png").scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio))
        
        name_label = QLabel(self.operatore_nome)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #333;")

        left_layout.addWidget(back_btn)
        left_layout.addWidget(user_icon)
        left_layout.addWidget(name_label)
        
        # CENTRO: Titolo
        title_label = QLabel("Gestione Matricole")
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
        central_frame.setStyleSheet("background-color: #c1c1c1;")
        central_layout = QVBoxLayout(central_frame)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setSpacing(15)

        # Header: Titolo sezione + Nuovo Detenuto + Aggiorna Lista
        header_row = QHBoxLayout()
        section_title = QLabel("Elenco Detenuti")
        section_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #444;")

        # Pulsante Nuovo Detenuto
        btn_new = QPushButton("➕ Nuovo Detenuto")
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
        btn_new.clicked.connect(self.nuovo_detenuto)

        # Pulsante Aggiorna Lista
        btn_refresh = QPushButton("🔄 Aggiorna Lista")
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
        # Importante: text color black altrimenti non si vede nella barra bianca
        icon_lens.setStyleSheet("color: black;") 
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca per Cognome, Nome o Matricola...")
        self.search_bar.setFont(QFont("Arial", 14))
        self.search_bar.setStyleSheet("border: none; background: transparent; color: black;")
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

        self.populate_list(self.detainees)

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
    def populate_list(self, data_list: list[DetenutoDTO]):
        for i in reversed(range(self.scroll_layout.count())):
            item = self.scroll_layout.itemAt(i)
            if item.widget(): item.widget().deleteLater()

        if not data_list:
            lbl = QLabel("Nessun detenuto trovato.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #333; font-size: 14px; padding-top: 20px;")
            self.scroll_layout.addWidget(lbl)
            return

        for det in data_list:
            row_frame = QFrame()
            row_frame.setFixedHeight(75)
            row_frame.setStyleSheet("background-color: white; border-radius: 15px;")
            row_layout = QHBoxLayout(row_frame)

            input_style = "background: #f7f7f7; border: 1px solid #bbb; border-radius: 8px; padding: 5px; color: black;"

            edt_cog = QLineEdit(det.cognome)
            edt_cog.setReadOnly(True)
            edt_cog.setStyleSheet(input_style)

            edt_nom = QLineEdit(det.nome)
            edt_nom.setReadOnly(True)
            edt_nom.setStyleSheet(input_style)

            edt_mat = QLineEdit(det.matricola)
            edt_mat.setReadOnly(True)
            edt_mat.setFixedWidth(110)
            edt_mat.setStyleSheet(input_style)

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
            btn_edit.clicked.connect(lambda checked, d=det: self.modifica_detenuto(d))

            row_layout.addWidget(edt_cog, stretch=2)
            row_layout.addWidget(edt_nom, stretch=2)
            row_layout.addWidget(edt_mat, stretch=1)
            row_layout.addWidget(btn_edit)

            self.scroll_layout.addWidget(row_frame)
        self.scroll_layout.addStretch()

    # ==========================================
    # NAVIGAZIONE E AZIONI
    # ==========================================
    def filter_list(self):
        testo = self.search_bar.text().lower().strip()
        filtrati = [d for d in self.detainees if testo in d.cognome.lower() or testo in d.nome.lower() or testo in d.matricola.lower()]
        self.populate_list(filtrati)

    def vai_indietro(self):
        """
        Torna alla finestra precedente.
        Se esiste un genitore salvato, lo mostra. Altrimenti crea una nuova istanza della Dashboard.
        """
        if self.parent_window:
            self.parent_window.show()
        else:
            # Fallback: istanzia di nuovo la dashboard principale
            try:
                # Sostituisci con il percorso corretto del tuo file principale
                from view.UfficiomatricoleView.UfficioLogin import MainWindow 
                self.home_window = MainWindow(self.session)
                self.home_window.show()
            except ImportError as e:
                # Stile messaggio errore leggibile
                err = QMessageBox(self)
                err.setText(f"Errore Navigazione: {e}")
                err.setStyleSheet("background-color: white; color: black;")
                err.exec()
                return

        self.close()

    def nuovo_detenuto(self):
        from view.UfficiomatricoleView.NuovoDetenutoView import NuovoDetenutoView
        # Passiamo self come parent
        self.form_nuovo = NuovoDetenutoView(session=self.session) 
        self.form_nuovo.show()

    def modifica_detenuto(self, det: DetenutoDTO):
        from view.UfficiomatricoleView.ModificaDetenuto import ModificaDetenuto
        self.edit_form = ModificaDetenuto(det.matricola, self.session) 
        self.edit_form.show()

    def logout(self):
        """
        Gestisce il logout con un popup stilizzato per essere leggibile
        anche con lo sfondo nero dell'app.
        """
        # Creiamo un box manuale per forzare lo stile
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Conferma Logout")
        msg_box.setText("Sei sicuro di voler uscire dal sistema?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        
        # Pulsanti Standard
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        # --- STILE CSS PER LEGGIBILITÀ SU SFONDO NERO ---
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                border: 2px solid #555;
            }
            QLabel {
                color: black;
                font-size: 14px;
                background-color: transparent;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Eseguiamo il box e controlliamo il risultato
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.session.current_user = None
            from view.LoginView.login_view import LoginWindow
            self.login_win = LoginWindow()
            self.login_win.show()
            self.close()

    def aggiorna_lista(self):
        try:
            self.detainees = self.load_detenuti()
            self.populate_list(self.detainees)
        except Exception as e:
            err = QMessageBox(self)
            err.setText(f"Impossibile aggiornare la lista:\n{e}")
            err.setStyleSheet("background-color: white; color: black;")
            err.exec()