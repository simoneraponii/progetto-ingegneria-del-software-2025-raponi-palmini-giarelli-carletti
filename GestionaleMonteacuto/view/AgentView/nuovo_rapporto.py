from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, 
    QPushButton, QHBoxLayout, QMessageBox, QFormLayout, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from app.session import Session
from controller.rapporto_controller import RapportoController

class NuovoRapportoDialog(QDialog):
    def __init__(self, session, codice_protocollo, rapporto_esistente=None, parent=None):
        super().__init__(parent)
        
        self.session = session
        self.codice_protocollo = codice_protocollo
        self.rapporto_esistente = rapporto_esistente # Se non è None, siamo in MODIFICA
        
        self.controller = RapportoController()
        
        # 1. Imposta Titolo Finestra e Bottone in base alla modalità
        mode_str = "Modifica" if self.rapporto_esistente else "Nuova"
        self.setWindowTitle(f"{mode_str} Rapporto Disciplinare - Prot. {self.codice_protocollo}")
        
        self.init_ui()
        
        # 2. SE SIAMO IN MODIFICA, PRE-POPOLIAMO I CAMPI
        if self.rapporto_esistente:
            self.txt_oggetto.setText(self.rapporto_esistente.oggetto)
            self.txt_descrizione.setText(self.rapporto_esistente.descrizione)
            self.btn_save.setText("Aggiorna Rapporto Disciplinare")

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Header
        lbl_header = QLabel("Gestione Segnalazione")
        lbl_header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        lbl_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_header.setStyleSheet("color: #007bff; margin-bottom: 10px;")
        main_layout.addWidget(lbl_header)

        # Container Form
        form_container = QFrame()
        form_container.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        form_layout_box = QVBoxLayout(form_container)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.txt_oggetto = QLineEdit()
        self.txt_oggetto.setPlaceholderText("Es. Rissa, Insulto, Rifiuto...")
        
        self.txt_descrizione = QTextEdit()
        self.txt_descrizione.setPlaceholderText("Descrizione dettagliata...")
        self.txt_descrizione.setMinimumHeight(150)
        
        form_layout.addRow("Oggetto:", self.txt_oggetto)
        form_layout.addRow("Dettagli:", self.txt_descrizione)
        
        form_layout_box.addLayout(form_layout)
        main_layout.addWidget(form_container)

        # Bottoni
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Annulla")
        btn_cancel.setStyleSheet("background-color: #e0e0e0; color: #333;")
        btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("Salva Rapporto Disciplinare")
        self.btn_save.setStyleSheet("background-color: #007bff; color: white;")
        self.btn_save.clicked.connect(self.tenta_salvataggio) 
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_save)
        main_layout.addLayout(btn_layout)

    def tenta_salvataggio(self):
        """Valida i dati E prova a salvare (Insert o Update) nel DB"""
        oggetto = self.txt_oggetto.text().strip()
        descrizione = self.txt_descrizione.toPlainText().strip()
        
        # 1. Validazione Campi
        if not oggetto or not descrizione:
            QMessageBox.warning(self, "Attenzione", "Compila tutti i campi.")
            return

        try:
            # 2. Decisione: MODIFICA o NUOVO?
            if self.rapporto_esistente:
                
                # --- LOGICA UPDATE ---
                success = self.controller.modifica_rapporto(self.rapporto_esistente.id, oggetto,descrizione)
                msg_success = "Rapporto aggiornato correttamente."
            else:
                # --- LOGICA INSERT ---
                success = self.controller.aggiungi_rapporto(oggetto, descrizione, self.session.current_user.username, self.codice_protocollo)
                msg_success = "Rapporto aggiunto con successo."
            
            # 3. Esito
            if success:
                QMessageBox.information(self, "Successo", msg_success)
                self.accept() 
            else:
                QMessageBox.warning(self, "Errore", "Operazione fallita sul database.")
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", str(e))