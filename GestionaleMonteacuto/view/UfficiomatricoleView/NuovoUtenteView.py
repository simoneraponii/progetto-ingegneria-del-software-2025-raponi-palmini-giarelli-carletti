# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QComboBox, QGridLayout, QScrollArea,
    QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# --- IMPORT ---
from controller.account_controller import AccountController
from app.session import Session
from model.enum.ruolo import Ruolo

class NuovoUtenteView(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.setWindowTitle("Sistema Penitenziario - Registrazione Staff")
        self.session = session
        self.controller = AccountController()
        
        self.resize(650, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        # --- PALETTE COLORI LIGHT ---
        self.setStyleSheet("""
            QWidget { 
                background-color: #F8F9FA; 
                font-family: 'Segoe UI', Arial; 
                font-size: 14px; 
            }
            QScrollArea { border: none; background: transparent; }
            QLabel { color: #202124; }
        """)

        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        
        self.setup_ui()

    def setup_ui(self):
        # --- HEADER ---
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #DADCE0;")
        h_layout = QHBoxLayout(header)
        
        title_label = QLabel("Registrazione Nuovo Staff")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1A73E8; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        h_layout.addWidget(title_label)
        self.window_layout.addWidget(header)

        # --- CONTENT AREA ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        
        form_layout = QVBoxLayout(container)
        form_layout.setContentsMargins(50, 30, 50, 30)
        form_layout.setSpacing(15)

        # 1. SEZIONE ANAGRAFICA (Nome e Cognome allineati)
        self.add_section_label(form_layout, "DATI ANAGRAFICI")
        card_anagrafica = self.create_card()
        grid_a = QGridLayout(card_anagrafica)
        grid_a.setContentsMargins(10, 10, 10, 10)
        
        self.input_nome = self.add_field(grid_a, "Nome", 0, 0)
        self.input_cognome = self.add_field(grid_a, "Cognome", 0, 1)
        form_layout.addWidget(card_anagrafica)

        # 2. SEZIONE CREDENZIALI (Username e Password allineati)
        self.add_section_label(form_layout, "ACCESSO E SICUREZZA")
        card_credenziali = self.create_card()
        grid_c = QGridLayout(card_credenziali)
        grid_c.setContentsMargins(10, 10, 10, 10)
        
        self.input_username = self.add_field(grid_c, "Username", 0, 0)
        
        # Campo Password allineato a destra di Username
        container_pass = QWidget()
        vbox_p = QVBoxLayout(container_pass)
        vbox_p.setContentsMargins(15, 10, 15, 10)
        lbl_p = QLabel("Password")
        lbl_p.setStyleSheet("font-weight: bold; color: #5F6368; font-size: 12px;")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setFixedHeight(38)
        self.input_password.setStyleSheet(self.field_style())
        vbox_p.addWidget(lbl_p)
        vbox_p.addWidget(self.input_password)
        grid_c.addWidget(container_pass, 0, 1)
        
        form_layout.addWidget(card_credenziali)

        # 3. SEZIONE RUOLO
        self.add_section_label(form_layout, "PERMESSI DI SISTEMA")
        card_ruolo = self.create_card()
        vbox_r = QVBoxLayout(card_ruolo)
        vbox_r.setContentsMargins(25, 15, 25, 20)
        
        lbl_ruolo = QLabel("Assegna Ruolo Operativo")
        lbl_ruolo.setStyleSheet("font-weight: bold; color: #5F6368; font-size: 12px;")
        
        self.combo_ruolo = QComboBox()
        self.combo_ruolo.setFixedHeight(38)
        self.combo_ruolo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #DADCE0;
                border-radius: 4px;
                padding-left: 10px;
                color: #202124;
            }
            QComboBox:hover { border: 1px solid #1A73E8; }
        """)
        
        self.popola_ruoli()
        vbox_r.addWidget(lbl_ruolo)
        vbox_r.addWidget(self.combo_ruolo)
        form_layout.addWidget(card_ruolo)

        form_layout.addStretch()

        # --- AZIONI ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.btn_cancel = QPushButton("Annulla")
        self.btn_cancel.setFixedSize(130, 45)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton { 
                background-color: white; 
                color: #5F6368; 
                border: 1px solid #DADCE0; 
                border-radius: 4px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #F1F3F4; }
        """)
        self.btn_cancel.clicked.connect(self.close)

        self.btn_save = QPushButton("REGISTRA UTENTE")
        self.btn_save.setFixedHeight(45)
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton { 
                background-color: #1A73E8; 
                color: white; 
                border-radius: 4px; 
                font-weight: bold; 
                font-size: 14px;
            }
            QPushButton:hover { background-color: #1765CC; }
        """)
        self.btn_save.clicked.connect(self.on_salva_click)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save, stretch=1)
        
        form_layout.addLayout(btn_layout)

        scroll.setWidget(container)
        self.window_layout.addWidget(scroll)

    # ==========================
    # HELPERS & STILI
    # ==========================
    def field_style(self):
        return """
            QLineEdit {
                background-color: white;
                border: 1px solid #DADCE0;
                border-radius: 4px;
                padding-left: 10px;
                color: #202124;
            }
            QLineEdit:focus { border: 2px solid #1A73E8; }
        """

    def create_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #E0E0E0; border-radius: 8px; }")
        return card

    def add_section_label(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #70757A; font-weight: bold; font-size: 11px; letter-spacing: 0.5px; margin-left: 5px;")
        layout.addWidget(lbl)

    def add_field(self, layout, label_text, row, col):
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(15, 10, 15, 10)
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight: bold; color: #5F6368; font-size: 12px;")
        field = QLineEdit()
        field.setFixedHeight(38)
        field.setStyleSheet(self.field_style())
        vbox.addWidget(lbl)
        vbox.addWidget(field)
        layout.addWidget(container, row, col)
        return field

    # ==========================
    # LOGICA
    # ==========================
    def popola_ruoli(self):
        self.combo_ruolo.clear()
        self.combo_ruolo.addItem("-- Seleziona un ruolo --", None)
        for r in Ruolo:
            self.combo_ruolo.addItem(r.name, r)

    def on_salva_click(self):
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        ruolo_selezionato = self.combo_ruolo.currentData()

        if not all([nome, cognome, username, password]) or ruolo_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Tutti i campi sono obbligatori.")
            return

        dati = {
            "nome": nome,
            "cognome": cognome,
            "username": username,
            "password": password,
            "ruolo": ruolo_selezionato,
            "tentativi": 3
        }

        try:
            if self.controller.create_utente(dati):
                QMessageBox.information(self, "Confermato", "Utente registrato nel sistema.")
                self.close()
            else:
                QMessageBox.warning(self, "Errore", "Username gia' presente.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))