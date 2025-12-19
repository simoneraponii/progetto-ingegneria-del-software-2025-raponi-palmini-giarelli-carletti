from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt
from View.AgentView import resources_rc
import sys
from View.AgentView.VisualizzaRapporto import VisualizzaRapportoWindow

class VisualizzaDetenutoWindow(QWidget):
    def __init__(self, nome, cogmome, matricola):
        super().__init__()
        self.setWindowTitle("Visualizza Verbali")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: gray; color: white;")

        self.detenuto_info = {
            "matricola": matricola,
            "nome": nome,
            "cognome": cogmome,
            "cf": "MLANBL80A01H501U",
            "fine_pena": "12/11/2028",
            "dettagli": "Condanna per reati contro la PA e spaccio internazionale"
        }
        self.lista_verbali = []

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(1)

        # Colonna sinistra
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(10, 10, 10, 10)
        left_panel.setSpacing(15)
        
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
        
        info_layout = QVBoxLayout()
        titolo = QLabel(f"DETENUTO ({self.detenuto_info['matricola']})")
        titolo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addStretch() 
        info_layout.addWidget(titolo)
        
        # Info detenuto 
        for label, value in [ 
            ("Nome", self.detenuto_info["nome"]), 
            ("Cognome", self.detenuto_info["cognome"]), 
            ("Codice Fiscale", self.detenuto_info["cf"]), 
            ("Data Fine Pena", self.detenuto_info["fine_pena"]), 
            ("Dettagli Pena", self.detenuto_info["dettagli"]) 
        ]: 
        
            l = QLabel(f"{label}: {value}") 
            l.setFont(QFont("Arial", 12)) 
            l.setWordWrap(True) 
            l.setAlignment(Qt.AlignmentFlag.AlignCenter) 
            info_layout.addWidget(l) 
            
        info_layout.addStretch()
        
        left_panel.addLayout(back_layout)  
        left_panel.addLayout(info_layout)    
        
        left_widget = QWidget() 
        left_widget.setLayout(left_panel) 
        left_widget.setFixedWidth(250)

        # Colonna centrale
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Colonna destra
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

        # Fusione delle 3 parti
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(right_widget)
        
    # Metodi
    def apri_rapporto(self, verbale):
        self.apri = VisualizzaRapportoWindow(verbale)
        self.apri.show()

    def crea_nuovo_verbale(self):
        nuovo_numero = len(self.lista_verbali) + 1
        nuovo_id = f"V{nuovo_numero:03d}"
        nuovo_verbale = {"id": nuovo_id, "confermato": False}
        self.lista_verbali.append(nuovo_verbale)
        self.aggiorna_centrale()

    def aggiorna_centrale(self):
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setSpacing(5)

        for i, verbale in enumerate(self.lista_verbali, start=1):
            box = QFrame()
            box.setStyleSheet("background-color: White; border-radius: 8px;")
            box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(5, 5, 5, 5)

            logo_label = QLabel()
            logo_label.setPixmap(QPixmap(":/Images/Images/verbale.png"))
            logo_label.setFixedSize(30, 30)
            logo_label.setScaledContents(True)

            numero = QLabel(f"Verbale n° {i}")
            numero.setStyleSheet("color: black;")
            numero.setFont(QFont("Arial", 14, QFont.Weight.Bold))

            logo_layout = QHBoxLayout()
            logo_layout.setSpacing(5)
            logo_layout.addWidget(logo_label)
            logo_layout.addWidget(numero)

            logo_widget = QWidget()
            logo_widget.setLayout(logo_layout)

            visualizza_btn = QPushButton("Visualizza rapporto")
            visualizza_btn.setStyleSheet("background-color: #666; color: white; padding: 6px;")
            visualizza_btn.clicked.connect(lambda _, v=verbale: self.apri_rapporto(v))

            stato_btn = QPushButton("Confermato" if verbale["confermato"] else "Non confermato")
            stato_btn.setStyleSheet("background-color: #888; color: white; padding: 4px; font-size: 10px;")
            stato_btn.setFixedWidth(120)

            box_layout.addWidget(logo_widget)
            box_layout.addWidget(visualizza_btn)
            box_layout.addWidget(stato_btn)
            central_layout.addWidget(box)

        self.scroll_area.setWidget(central_widget)
        