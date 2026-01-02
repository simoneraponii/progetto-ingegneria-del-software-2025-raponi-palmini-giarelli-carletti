import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy, QInputDialog
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt

from view.AgentView import resources_rc


from controller.detenuti_controller import DetenutiController
from controller.rapporto_controller import RapportoController
from model.enum.stato_verbale import StatoVerbale
from view.AgentView.visualizza_verbale import VisualizzaVerbaleWindow

class VisualizzaDetenutoWindow(QWidget):
    def __init__(self, session, matricola: str):
        super().__init__()
        
        # 1. DATI E SESSIONE
        self.session = session
        self.matricola_target = matricola
        
        self.controller = DetenutiController()
        self.rapporto_controller = RapportoController()
        
        self.detenuto = None
        self.lista_verbali = []

        # 2. SETUP FINESTRA
        self.setWindowTitle(f"Visualizza Verbali - {matricola}")
        self.resize(1100, 650)
        self.setStyleSheet("background-color: gray; color: white;")

        # 3. CARICAMENTO DATI DAL DB
        self.load_data()

        # 4. GUI
        self.init_ui()

    def load_data(self):
        try:
            self.detenuto = self.controller.get_detenuto(self.matricola_target)
            
            if not self.detenuto:
                QMessageBox.critical(self, "Errore", "Detenuto non trovato.")
                self.close()
                return

            self.lista_verbali = self.rapporto_controller.get_verbali_detenuto(self.matricola_target)

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore caricamento dati: {e}")

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(1)

        # ==========================================
        # COLONNA SINISTRA (INFO DETENUTO)
        # ==========================================
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(10, 10, 10, 10)
        left_panel.setSpacing(15)
        
        # Tasto Indietro
        back_layout = QHBoxLayout()
        back_btn = QPushButton()
        back_btn.setIcon(QIcon.fromTheme("go-previous"))
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: lightGray;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #444;
                border-radius: 20px;
            }
        """)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.close)
        back_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Info Layout
        info_layout = QVBoxLayout()
        
        # Titolo con Matricola
        lbl_matr = self.detenuto.matricola if self.detenuto else self.matricola_target
        titolo = QLabel(f"DETENUTO\n({lbl_matr})")
        titolo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addStretch() 
        info_layout.addWidget(titolo)
        
        # Preparazione Dati per il Loop
        if self.detenuto:
            d = self.detenuto
            # Uso getattr per sicurezza
            nome = getattr(d.dati_anagrafici, 'nome', '-')
            cognome = getattr(d.dati_anagrafici, 'cognome', '-')
            cf = getattr(d.dati_anagrafici, 'codice_fiscale', '-')
            
            fine_pena = str(getattr(d.pena, 'data_fine', getattr(d.pena, 'dataFinePena', '-')))
            reato = getattr(d.pena, 'reato', getattr(d.pena, 'descrizione', '-'))
            
            ala = getattr(d.ubicazione, 'sezione', '-')
            cella = getattr(d.ubicazione, 'numero_cella', getattr(d.ubicazione, 'camera', '-'))
            locazione_str = f"Ala {ala} - Cella {cella}"

            dati_da_mostrare = [
                ("Nome", nome),
                ("Cognome", cognome),
                ("Codice Fiscale", cf),
                ("Ubicazione", locazione_str),
                ("Fine Pena", fine_pena),
                ("Dettagli Pena", reato)
            ]
        else:
            dati_da_mostrare = [("Stato", "Errore caricamento")]

        # Loop generazione Label
        for label, value in dati_da_mostrare: 
            l = QLabel(f"{label}:\n{value}") 
            l.setFont(QFont("Arial", 11)) 
            l.setWordWrap(True) 
            l.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            l.setStyleSheet("border-bottom: 1px solid #555; padding-bottom: 5px;")
            info_layout.addWidget(l) 
            info_layout.addSpacing(5)
            
        info_layout.addStretch()
        
        left_panel.addLayout(back_layout)  
        left_panel.addLayout(info_layout)    
        
        left_widget = QWidget() 
        left_widget.setLayout(left_panel) 
        left_widget.setFixedWidth(250)

        # ==========================================
        # COLONNA CENTRALE (LISTA VERBALI)
        # ==========================================
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.scroll_content)

        # Popolo la lista iniziale
        self.aggiorna_centrale()

        # ==========================================
        # COLONNA DESTRA (AZIONI)
        # ==========================================
        right_panel = QVBoxLayout()
        
        nuovo_btn = QPushButton(" Nuovo Verbale")
        nuovo_btn.setIcon(QIcon(":/Images/Images/nuovoV.png"))
        nuovo_btn.clicked.connect(self.crea_nuovo_verbale)
        nuovo_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """)
        nuovo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        nuovo_btn.setFixedWidth(150)
        
        right_panel.addWidget(nuovo_btn, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        right_panel.addStretch()
        
        crest = QLabel()
        crest.setPixmap(QPixmap(":/Images/Images/logo.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        
        right_panel.addStretch()
        right_panel.addWidget(crest, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setFixedWidth(200)

        # FUSIONE LAYOUT
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(right_widget)

    # ==========================================
    # LOGICA
    # ==========================================
    def apri_verbale(self, verbale):
        """Apre il dettaglio del verbale (lista note + tasti conferma)"""
        # Passiamo la sessione corrente e l'oggetto verbale selezionato
        self.apri = VisualizzaVerbaleWindow(self.session, verbale)
        self.apri.show()

    def crea_nuovo_verbale(self):
        titolo, ok = QInputDialog.getText(self, "Nuovo Verbale", "Inserisci il titolo del verbale:")
        try:
            if ok and titolo:
                if self.rapporto_controller.crea_verbale(titolo, self.detenuto.matricola):
                    self.aggiorna_centrale()
                    QMessageBox.information(self, "Confermato", "Verbale registrato nel sistema.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))
        
    def aggiorna_centrale(self):
        # 1. Pulizia widget precedenti
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        # 2. Ricarica dati
        try:
            self.lista_verbali = self.rapporto_controller.get_verbali_detenuto(self.matricola_target)
        except Exception as e:
            print(f"Errore refresh: {e}")
            self.lista_verbali = []

        if not self.lista_verbali:
            lbl = QLabel("Nessun verbale presente a sistema.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: white; font-style: italic; font-size: 14px; margin-top: 20px;")
            self.scroll_layout.addWidget(lbl)
            return

        # 3. Generazione Card
        for verbale in self.lista_verbali:
            box = QFrame()
            box.setStyleSheet("""
                QFrame {
                    background-color: white; 
                    border-radius: 10px; 
                    border: 1px solid #ccc;
                }
            """)
            box.setFixedHeight(120) 
            box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(15, 10, 15, 10)
            box_layout.setSpacing(5)

            # --- RIGA 1: PROTOCOLLO E TITOLO ---
            row_top = QHBoxLayout()
            
            # Icona
            icon_lbl = QLabel()
            icon_lbl.setPixmap(QPixmap(":/Images/Images/verbale.png").scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio))
            
            # Info Testuali
            info_col = QVBoxLayout()
            info_col.setSpacing(2)
            
            lbl_prot = QLabel(f"Protocollo: {verbale.codice_protocollo}")
            lbl_prot.setStyleSheet("color: #000; font-weight: bold; font-size: 15px;")
            
            lbl_titolo = QLabel(verbale.titolo) # Titolo inserito dall'utente
            lbl_titolo.setStyleSheet("color: #555; font-size: 13px;")
            
            info_col.addWidget(lbl_prot)
            info_col.addWidget(lbl_titolo)
            
            row_top.addWidget(icon_lbl)
            row_top.addSpacing(10)
            row_top.addLayout(info_col)
            row_top.addStretch()
            
            # --- RIGA 2: AZIONI E STATO ---
            row_bottom = QHBoxLayout()
            
            # Bottone Visualizza (Apre la lista dei rapporti interni)
            btn_details = QPushButton("Apri Fascicolo Verbale")
            btn_details.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_details.setIcon(QIcon(":/Images/Images/search.png")) 
            btn_details.setStyleSheet("""
                QPushButton {
                    background-color: #0056b3; 
                    color: white; 
                    border-radius: 5px; 
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #004494; }
            """)
            # Qui colleghiamo l'apertura della nuova finestra
            btn_details.clicked.connect(lambda _, v=verbale: self.apri_verbale(v))

            # --- LOGICA STATI (Normalizzazione a Enum) ---
            stato_enum = verbale.stato_verbale
            # Se arriva come stringa, convertiamo
            if isinstance(stato_enum, str):
                try: stato_enum = StatoVerbale[stato_enum]
                except: stato_enum = None
            
            # Default values (Unknown)
            stato_text = "STATO SCONOSCIUTO"
            bg_color = "#E2E3E5"
            text_color = "#383D41"
            border_color = "#D6D8DB"

            if stato_enum == StatoVerbale.CREATED:
                stato_text = "BOZZA"
                bg_color = "#FFF3CD" # Giallo chiaro
                text_color = "#856404"
                border_color = "#FFEEBA"
            
            elif stato_enum == StatoVerbale.CONFIRMED_UFFICIO_COMANDO:
                stato_text = "CONFERMATO UFF. COMANDO"
                bg_color = "#D1ECF1" # Azzurro chiaro
                text_color = "#0C5460"
                border_color = "#B8DAFF"
                
            elif stato_enum == StatoVerbale.CONFIRMED_COMANDANTE:
                stato_text = "APPROVATO (CHIUSO)"
                bg_color = "#D4EDDA" # Verde chiaro
                text_color = "#155724"
                border_color = "#C3E6CB"

            lbl_stato = QLabel(stato_text)
            lbl_stato.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_stato.setFixedSize(160, 30)
            lbl_stato.setStyleSheet(f"""
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 15px;
                font-weight: bold;
                font-size: 11px;
            """)

            row_bottom.addWidget(btn_details)
            row_bottom.addStretch()
            row_bottom.addWidget(lbl_stato)

            box_layout.addLayout(row_top)
            box_layout.addLayout(row_bottom)
            
            self.scroll_layout.addWidget(box)