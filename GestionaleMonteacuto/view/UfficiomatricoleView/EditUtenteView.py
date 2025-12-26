# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QComboBox, QGridLayout, QScrollArea,
    QMessageBox, QCheckBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from controller.account_controller import AccountController
from app.session import Session
from model.enum.ruolo import Ruolo

class EditUtenteView(QWidget):
    def __init__(self, session: Session, username_target: str):
        super().__init__()
        self.setWindowTitle(f"Modifica Utente: {username_target}")
        self.session = session
        self.username_target = username_target
        self.controller = AccountController()
        
        self.resize(650, 650)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.setStyleSheet("""
            QWidget { background-color: #F8F9FA; font-family: 'Segoe UI', Arial; font-size: 14px; }
            QScrollArea { border: none; background: transparent; }
            QLabel { color: #202124; }
        """)

        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_ui()
        self.carica_dati_utente()

    def setup_ui(self):
        # --- HEADER ---
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: white; border-bottom: 1px solid #DADCE0;")
        h_layout = QHBoxLayout(header)
        
        title_label = QLabel(f"Profilo Utente: {self.username_target}")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1A73E8; border: none;")
        h_layout.addWidget(title_label)
        self.window_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form_layout = QVBoxLayout(container)
        form_layout.setContentsMargins(50, 20, 50, 20)
        form_layout.setSpacing(15)

        # 1. CREDENZIALI (Username Bloccato)
        self.add_section_label(form_layout, "ACCOUNT (NON MODIFICABILE)")
        card_account = self.create_card()
        grid_acc = QGridLayout(card_account)
        
        self.input_username = self.add_field(grid_acc, "Username", 0, 0)
        self.input_username.setReadOnly(True)
        self.input_username.setStyleSheet(self.input_username.styleSheet() + "background-color: #E8EAED; color: #5F6368;")
        
        self.input_password = self.add_field(grid_acc, "Nuova Password", 0, 1)
        self.input_password.setPlaceholderText("Lascia vuoto per non cambiare")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(card_account)

        # 2. ANAGRAFICA
        self.add_section_label(form_layout, "DATI PERSONALI")
        card_anagrafica = self.create_card()
        grid_ana = QGridLayout(card_anagrafica)
        self.input_nome = self.add_field(grid_ana, "Nome", 0, 0)
        self.input_cognome = self.add_field(grid_ana, "Cognome", 0, 1)
        form_layout.addWidget(card_anagrafica)

        # 3. STATO E RUOLO
        self.add_section_label(form_layout, "STATO E PERMESSI")
        card_stato = self.create_card()
        hbox_stato = QHBoxLayout(card_stato)
        hbox_stato.setContentsMargins(20, 15, 20, 15)

        # Combo Ruolo
        vbox_ruolo = QVBoxLayout()
        vbox_ruolo.addWidget(QLabel("Ruolo"))
        self.combo_ruolo = QComboBox()
        self.combo_ruolo.setFixedHeight(38)
        self.popola_ruoli()
        vbox_ruolo.addWidget(self.combo_ruolo)
        hbox_stato.addLayout(vbox_ruolo, stretch=2)

        # Switch Stato (Tentativi)
        vbox_switch = QVBoxLayout()
        vbox_switch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stato_testo = QLabel("Stato: Attivo")
        self.lbl_stato_testo.setStyleSheet("font-weight: bold; color: #1E8E3E;")
        
        self.switch_stato = QCheckBox("Attivo/Bloccato")
        self.switch_stato.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_stato.setChecked(True)
        self.switch_stato.toggled.connect(self.aggiorna_label_stato)
        
        vbox_switch.addWidget(self.lbl_stato_testo)
        vbox_switch.addWidget(self.switch_stato)
        hbox_stato.addLayout(vbox_switch, stretch=1)
        
        form_layout.addWidget(card_stato)

        # --- BOTTONI ---
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("SALVA MODIFICHE")
        self.btn_save.setFixedHeight(45)
        self.btn_save.setStyleSheet("QPushButton { background-color: #1A73E8; color: white; border-radius: 4px; font-weight: bold; }")
        self.btn_save.clicked.connect(self.on_save_click)
        
        self.btn_cancel = QPushButton("Annulla")
        self.btn_cancel.setFixedSize(100, 45)
        self.btn_cancel.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        form_layout.addLayout(btn_layout)

        scroll.setWidget(container)
        self.window_layout.addWidget(scroll)

    def aggiorna_label_stato(self, checked):
        if checked:
            self.lbl_stato_testo.setText("Stato: Attivo")
            self.lbl_stato_testo.setStyleSheet("font-weight: bold; color: #1E8E3E;")
        else:
            self.lbl_stato_testo.setText("Stato: Bloccato")
            self.lbl_stato_testo.setStyleSheet("font-weight: bold; color: #D93025;")

    def carica_dati_utente(self):
        # Recupera l'utente dal controller tramite username
        utente = self.controller.get_by_username(self.username_target)
        if utente:
            self.input_username.setText(utente.username)
            self.input_nome.setText(utente.nome)
            self.input_cognome.setText(utente.cognome)
            # Imposta Switch basato sui tentativi
            self.switch_stato.setChecked(utente.tentativi > 0)
            # Imposta Ruolo nella combo
            index = self.combo_ruolo.findData(utente.ruolo)
            if index != -1:
                self.combo_ruolo.setCurrentIndex(index)
            else:
                # fallback di sicurezza
                self.combo_ruolo.setCurrentIndex(0)

    def popola_ruoli(self):
        for r in Ruolo:
            self.combo_ruolo.addItem(r.name, r)

    def on_save_click(self):
        # Se lo switch e' attivo invia 3, altrimenti 0
        tentativi_val = 3 if self.switch_stato.isChecked() else 0
        
        dati = {
            "username": self.username_target,
            "nome": self.input_nome.text().strip(),
            "cognome": self.input_cognome.text().strip(),
            "password": self.input_password.text().strip(), # Se vuota, il controller non la aggiorna
            "ruolo": self.combo_ruolo.currentData().name,
            "tentativi": tentativi_val
        }

        password = self.input_password.text().strip()
        if password:
            dati["password"] = password

        if self.controller.update_utente(self.username_target,dati):
            QMessageBox.information(self, "Successo", "Profilo aggiornato correttamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Errore", "Impossibile aggiornare l'utente.")

    # --- HELPERS GRAFICI (STESSI DELLA NUOVOUTENTEVIE) ---
    def create_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border: 1px solid #E0E0E0; border-radius: 8px; }")
        return card

    def add_section_label(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #70757A; font-weight: bold; font-size: 11px; margin-left: 5px;")
        layout.addWidget(lbl)

    def add_field(self, layout, label_text, row, col):
        container = QWidget()
        vbox = QVBoxLayout(container)
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight: bold; color: #5F6368; font-size: 12px;")
        field = QLineEdit()
        field.setFixedHeight(38)
        field.setStyleSheet("border: 1px solid #DADCE0; border-radius: 4px; padding-left: 10px;")
        vbox.addWidget(lbl)
        vbox.addWidget(field)
        layout.addWidget(container, row, col)
        return field


