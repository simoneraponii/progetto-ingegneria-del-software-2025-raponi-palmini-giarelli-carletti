# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QTextEdit, QDateEdit, QGridLayout, QScrollArea,
    QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate

from controller.detenuti_controller import DetenutiController
from app.session import Session

class ModificaDetenuto(QWidget):
    def __init__(self, matricola_detenuto, session: Session = None):
        super().__init__()
        self.setWindowTitle("Modifica Detenuto")
        self.detenuti_controller = DetenutiController()
        self.session = session
        self.matricola_id = matricola_detenuto
        
        self.resize(950, 750)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.setStyleSheet("""
            QWidget { background-color: #F4F6F9; font-family: 'Segoe UI'; font-size: 14px; color: #333; }
            QScrollArea { border: none; background-color: #F4F6F9; }
        """)

        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()
        self.carica_dati()

    def setup_ui(self):
        # --- HEADER ---
        header = QFrame()
        header.setFixedHeight(65)
        header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        h_layout = QHBoxLayout(header)
        title_label = QLabel(f"Modifica Profilo Detenuto")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        h_layout.addWidget(title_label)
        self.window_layout.addWidget(header)

        # --- CONTENT ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        form_layout = QVBoxLayout(container)
        form_layout.setContentsMargins(30, 20, 30, 30)
        form_layout.setSpacing(15)

        # SEZIONE ANAGRAFICA
        self.add_section_title(form_layout, "DATI ANAGRAFICI")
        card_a = self.create_card()
        grid_a = QGridLayout(card_a)
        
        self.input_nome = self.add_field(grid_a, "Nome", 0, 0)
        self.input_cognome = self.add_field(grid_a, "Cognome", 0, 1)
        self.input_luogo_nascita = self.add_field(grid_a, "Luogo di Nascita", 0, 2)
        
        self.input_cf = self.add_field(grid_a, "Codice Fiscale", 1, 0)
        self.input_data_nascita = self.add_date_field(grid_a, "Data di Nascita", 1, 1)
        self.input_matricola = self.add_field(grid_a, "Matricola", 1, 2)
        self.input_matricola.setReadOnly(True)
        self.input_matricola.setStyleSheet("background-color: #EEE; border: 1px solid #CCC; border-radius: 4px; padding-left: 10px;")

        # SEZIONE UBICAZIONE
        self.add_section_title(form_layout, "UBICAZIONE")
        card_u = self.create_card()
        grid_u = QGridLayout(card_u)
        self.input_sezione = self.add_field(grid_u, "Sezione", 0, 0)
        self.input_camera = self.add_field(grid_u, "Camera", 0, 1)

        # SEZIONE PENA
        self.add_section_title(form_layout, "DETTAGLI PENA")
        card_p = self.create_card()
        grid_p = QGridLayout(card_p)
        self.input_fine_pena = self.add_date_field(grid_p, "Data Fine Pena", 0, 0)
        
        self.text_accuse = QTextEdit()
        self.text_accuse.setPlaceholderText("Descrizione reati...")
        self.text_accuse.setFixedHeight(100)
        self.text_accuse.setStyleSheet("background: white; border: 1px solid #CCC; border-radius: 4px; padding: 8px;")
        
        form_layout.addWidget(card_a)
        form_layout.addWidget(card_u)
        form_layout.addWidget(card_p)
        form_layout.addWidget(QLabel("Note e Accuse:"))
        form_layout.addWidget(self.text_accuse)

        # BOTTONI
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("SALVA MODIFICHE")
        self.btn_save.setFixedSize(220, 45)
        self.btn_save.setStyleSheet("background-color: #0078D4; color: white; font-weight: bold; border-radius: 6px;")
        self.btn_save.clicked.connect(self.on_salva_click)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        form_layout.addLayout(btn_layout)

        self.input_cf.setReadOnly(True)
        self.input_cf.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.input_cf.setStyleSheet("""
            background-color: #EEE;
            border: 1px solid #CCC;
            border-radius: 4px;
            padding-left: 10px;
            color: #666;
        """)

        scroll.setWidget(container)
        self.window_layout.addWidget(scroll)

    def carica_dati(self):
        try:
            # Chiamata al tuo DAO tramite controller
            d = self.detenuti_controller.get_detenuto(self.matricola_id)
            if d:
                # Popolamento Anagrafica
                self.input_nome.setText(d.dati_anagrafici.nome)
                self.input_cognome.setText(d.dati_anagrafici.cognome)
                self.input_cf.setText(d.dati_anagrafici.codice_fiscale)
                self.input_luogo_nascita.setText(d.dati_anagrafici.luogo_nascita)
                dt_nasc = d.dati_anagrafici.data_nascita
                self.input_data_nascita.setDate(QDate(dt_nasc.year, dt_nasc.month, dt_nasc.day))
                self.input_matricola.setText(self.matricola_id)
                # Popolamento Ubicazione
                self.input_sezione.setText(d.ubicazione.sezione)
                self.input_camera.setText(d.ubicazione.camera)
                
                # Popolamento Pena
                dt_pena = d.pena.dataFinePena
                self.input_fine_pena.setDate(QDate(dt_pena.year, dt_pena.month, dt_pena.day))
                self.text_accuse.setPlainText(d.pena.descrizione)


        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nel caricamento dati: {e}")

    def on_salva_click(self):
        # Creiamo un dizionario coerente con la struttura Detenuto prevista dal controller
        dati = {
            "dati_anagrafici": {
                "nome": self.input_nome.text().strip(),
                "cognome": self.input_cognome.text().strip(),
                "codiceFiscale": self.input_cf.text().strip().upper(),
                "luogoNascita": self.input_luogo_nascita.text().strip(),
                "dataNascita": self.input_data_nascita.date().toString("yyyy-MM-dd")
            },
            "ubicazione": {
                "sezione": self.input_sezione.text().strip(),
                "camera": self.input_camera.text().strip()
            },
            "pena": {
                "descrizione": self.text_accuse.toPlainText().strip(),
                "dataFinePena": self.input_fine_pena.date().toString("yyyy-MM-dd")
            }
        }
        try:
            # Chiamata al controller
            successo = self.detenuti_controller.update_detenuto(self.matricola_id, dati)
            if successo:
                QMessageBox.information(self, "Successo", "Dati aggiornati correttamente!")
                self.close()
            else:
                QMessageBox.warning(self, "Attenzione", "Impossibile aggiornare i dati.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nel salvataggio: {e}")




    # --- HELPERS ---
    def add_section_title(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #5F6368; font-weight: bold; font-size: 12px; margin-top: 10px;")
        layout.addWidget(lbl)

    def create_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #FFFFFF; border: 1px solid #DCE1E7; border-radius: 8px; }")
        return card

    def add_field(self, layout, label_text, row, col):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(label_text))
        f = QLineEdit()
        f.setFixedHeight(35)
        f.setStyleSheet("background: white; border: 1px solid #CCC; border-radius: 4px; padding-left: 10px;")
        vbox.addWidget(f)
        layout.addLayout(vbox, row, col)
        return f

    def add_date_field(self, layout, label_text, row, col):
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(label_text))
        d = QDateEdit()
        d.setCalendarPopup(True)
        d.setFixedHeight(35)
        d.setDisplayFormat("dd/MM/yyyy")
        d.setStyleSheet("background: white; border: 1px solid #CCC; border-radius: 4px; padding-left: 10px;")
        vbox.addWidget(d)
        layout.addLayout(vbox, row, col)
        return d