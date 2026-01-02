import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QMessageBox, QSizePolicy, QDialog
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

from app.session import Session
from controller.rapporto_controller import RapportoController

# IMPORTIAMO GLI ENUM
from model.enum.stato_verbale import StatoVerbale
from model.enum.ruolo import Ruolo
from model.rapporti.verbale import Verbale

class VisualizzaVerbaleWindow(QWidget):
    def __init__(self, session: Session, verbale_oggetto: Verbale):
        super().__init__()
        
        self.session = session
        self.verbale = verbale_oggetto 
        self.codice_protocollo = verbale_oggetto.codice_protocollo
        
        self.controller = RapportoController()
        self.lista_rapporti = []
        
        self.setWindowTitle(f"Fascicolo Verbale - {self.codice_protocollo}")
        self.resize(950, 700)
        self.setStyleSheet("background-color: #dcdcdc; color: #333;")

        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # HEADER
        header_layout = QHBoxLayout()
        
        btn_back = QPushButton("<- Indietro")
        btn_back.setFixedSize(100, 40)
        btn_back.setStyleSheet("background-color: #555; color: white; border-radius: 5px; font-weight: bold;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.close)
        
        center_info = QVBoxLayout()
        center_info.setSpacing(5)
        
        lbl_title = QLabel(f"PROTOCOLLO: {self.codice_protocollo}")
        lbl_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_stato_header = QLabel("Caricamento...")
        self.lbl_stato_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stato_header.setFixedSize(200, 30)
        
        center_info.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)
        center_info.addWidget(self.lbl_stato_header, alignment=Qt.AlignmentFlag.AlignCenter)

        right_actions = QVBoxLayout()
        
        # MODIFICA 1: self.btn_add per poterlo nascondere
        self.btn_add = QPushButton("+ Aggiungi Rapporto")
        self.btn_add.setFixedSize(160, 35)
        self.btn_add.setStyleSheet("background-color: #007bff; color: white; border-radius: 5px; font-weight: bold;")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.clicked.connect(self.action_aggiungi_rapporto)
        
        self.btn_conferma = QPushButton("OK CONFERMA VERBALE")
        self.btn_conferma.setFixedSize(160, 35)
        self.btn_conferma.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_conferma.clicked.connect(self.action_conferma_verbale)
        self.btn_conferma.setVisible(False) 

        right_actions.addWidget(self.btn_add)
        right_actions.addWidget(self.btn_conferma)

        header_layout.addWidget(btn_back)
        header_layout.addStretch()
        header_layout.addLayout(center_info)
        header_layout.addStretch()
        header_layout.addLayout(right_actions)
        
        main_layout.addLayout(header_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Gestione iniziale stato
        stato_iniziale = self.verbale.stato_verbale
        if isinstance(stato_iniziale, str):
            try: stato_iniziale = StatoVerbale[stato_iniziale]
            except: stato_iniziale = None
            
        self.aggiorna_grafica_stato(stato_iniziale)
        self.check_permessi_conferma()

    def _get_current_role_enum(self):
        ruolo = self.session.current_user.ruolo
        if isinstance(ruolo, str):
            try: 
                return Ruolo[ruolo]
            except KeyError: 
                return None
        return ruolo

    def check_permessi_conferma(self):
        ruolo = self._get_current_role_enum()
        stato = self.verbale.stato_verbale
        if isinstance(stato, str):
            try: stato = StatoVerbale[stato]
            except: stato = None
        if stato == StatoVerbale.CONFIRMED_COMANDANTE:
            self.btn_add.setVisible(False)
        else:
            self.btn_add.setVisible(True)

        can_approve = False
        btn_text = ""
        btn_style = ""

        if ruolo == Ruolo.UFFICIO_COMANDO and stato == StatoVerbale.CREATED:
            can_approve = True
            btn_text = "CONFERMA VERBALE"
            btn_style = "background-color: #17a2b8; color: white; border-radius: 5px; font-weight: bold;"

        elif ruolo == Ruolo.COMANDANTE and stato == StatoVerbale.CONFIRMED_UFFICIO_COMANDO:
            can_approve = True
            btn_text = "APPROVAZIONE FINALE"
            btn_style = "background-color: #28a745; color: white; border-radius: 5px; font-weight: bold;"

        self.btn_conferma.setVisible(can_approve)
        if can_approve:
            self.btn_conferma.setText(btn_text)
            self.btn_conferma.setStyleSheet(btn_style)

    def aggiorna_grafica_stato(self, stato_enum):
        if isinstance(stato_enum, str):
            try: stato_enum = StatoVerbale[stato_enum]
            except: stato_enum = None

        if stato_enum == StatoVerbale.CREATED:
            text, col, bg = "BOZZA / IN LAVORAZIONE", "#856404", "#FFF3CD"
        elif stato_enum == StatoVerbale.CONFIRMED_UFFICIO_COMANDO:
            text, col, bg = "CONFERMATO UFF. COMANDO", "#0C5460", "#D1ECF1"
        elif stato_enum == StatoVerbale.CONFIRMED_COMANDANTE:
            text, col, bg = "CONFERMATO (CHIUSO)", "#155724", "#D4EDDA"
        else:
            text, col, bg = "STATO SCONOSCIUTO", "#333", "#ccc"

        self.lbl_stato_header.setText(text)
        self.lbl_stato_header.setStyleSheet(f"""
            background-color: {bg}; 
            color: {col}; 
            border-radius: 15px; 
            font-weight: bold;
            border: 1px solid {col};
        """)
        if stato_enum:
             self.verbale.stato_verbale = stato_enum.name

    def action_conferma_verbale(self):
        confirm = QMessageBox.question(
            self, "Conferma Operazione", 
            "Confermi di voler procedere con la conferma del verbale?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.No:
            return

        ruolo_attuale = self._get_current_role_enum()
        
        success = self.controller.conferma_verbale(self.codice_protocollo, ruolo_attuale)
        
        if not success:
            QMessageBox.critical(self, "Errore", "Impossibile aggiornare lo stato nel database.")
            return

        # GUI Update
        nuovo_stato_enum = self.controller.get_stato_attuale(self.codice_protocollo)
        self.aggiorna_grafica_stato(nuovo_stato_enum)
        self.check_permessi_conferma() 

        # Form Nota Automatica
        from view.AgentView.nuovo_rapporto import NuovoRapportoDialog
        dialog = NuovoRapportoDialog(self.session, self.codice_protocollo, parent=self)
        
        # Testi personalizzati mantenuti come richiesto
        if ruolo_attuale == Ruolo.UFFICIO_COMANDO:
            oggetto_auto = f"Conferma verbale {self.verbale.codice_protocollo} di primo livello"
            descrizione_auto = f"Conferma apposta in data odierna da {self.session.current_user.cognome} {self.session.current_user.nome}"
        else:
            oggetto_auto = f"Conferma finale verbale {self.verbale.codice_protocollo}"
            descrizione_auto = f"Conferma apposta in data odierna dal comandante {self.session.current_user.cognome} {self.session.current_user.nome}"

        dialog.txt_oggetto.setText(oggetto_auto)
        dialog.txt_descrizione.setText(descrizione_auto)
        dialog.exec()
        
        self.load_data()

    def load_data(self):
        try:
            self.lista_rapporti = self.controller.get_lista_rapporti(self.codice_protocollo)
            self.populate_ui()
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

    def populate_ui(self):
        for i in reversed(range(self.scroll_layout.count())): 
            w = self.scroll_layout.itemAt(i).widget()
            if w: w.setParent(None)

        if not self.lista_rapporti:
            lbl = QLabel("Nessun rapporto disciplinare presente.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #666; font-style: italic; margin-top: 40px;")
            self.scroll_layout.addWidget(lbl)
            return
        
        ruolo = self._get_current_role_enum()
        is_comandante = (ruolo == Ruolo.COMANDANTE)
        
        
        is_closed = False
        stato = self.verbale.stato_verbale
        if isinstance(stato, str):
             try: is_closed = (StatoVerbale[stato] == StatoVerbale.CONFIRMED_COMANDANTE)
             except: pass
        else:
             is_closed = (stato == StatoVerbale.CONFIRMED_COMANDANTE)

        for rapporto in self.lista_rapporti:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: white; 
                    border-radius: 10px; 
                    border: 1px solid #bbb;
                }
            """)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            
            layout_card = QVBoxLayout(card)
            layout_card.setContentsMargins(15, 15, 15, 15)
            
            row_top = QHBoxLayout()
            
            lbl_obj = QLabel(rapporto.oggetto)
            lbl_obj.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            lbl_obj.setStyleSheet("color: #D93025;")
            
            row_top.addWidget(lbl_obj)
            row_top.addStretch()

            if is_comandante and not is_closed:
                btn_edit = QPushButton("Modifica")
                btn_edit.setFixedSize(80, 25)
                btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_edit.setStyleSheet("""
                    QPushButton {
                        background-color: #ffc107; color: #333; border-radius: 4px; font-weight: bold; font-size: 11px;
                    }
                    QPushButton:hover { background-color: #e0a800; }
                """)
                btn_edit.clicked.connect(lambda _, r=rapporto: self.action_modifica_rapporto(r))
                row_top.addWidget(btn_edit)
                row_top.addSpacing(10) 
            
            lbl_data = QLabel(str(rapporto.data))
            lbl_data.setStyleSheet("color: #666;")
            row_top.addWidget(lbl_data)
            
            lbl_autore = QLabel(f"Agente: {rapporto.fk_username}")
            lbl_autore.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            lbl_autore.setStyleSheet("color: #444; margin-bottom: 5px;")

            lbl_desc = QLabel(rapporto.descrizione)
            lbl_desc.setWordWrap(True)
            
            layout_card.addLayout(row_top)
            layout_card.addWidget(lbl_autore)
            layout_card.addWidget(lbl_desc)
            
            self.scroll_layout.addWidget(card)

    def action_modifica_rapporto(self, rapporto):
        from view.AgentView.nuovo_rapporto import NuovoRapportoDialog
        dialog = NuovoRapportoDialog(self.session, self.codice_protocollo, rapporto_esistente=rapporto, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def action_aggiungi_rapporto(self):
        from view.AgentView.nuovo_rapporto import NuovoRapportoDialog
        dialog = NuovoRapportoDialog(self.session, self.codice_protocollo, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()