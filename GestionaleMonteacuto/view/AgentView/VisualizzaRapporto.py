from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy, QDialog, QTextEdit
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt, QSize
from view.AgentView import resources_rc
import sys
from view.AgentView.AggiungiRapporto import AggiungiRapportoWindow

detenuto_info = {}
lista_verbali = []
rapporti = []

class VisualizzaRapportoWindow(QWidget):
    def __init__(self, verbale):
        super().__init__()
        self.verbale = verbale
        # Ogni verbale ha la sua lista indipendente
        self.rapporti_disciplinari = verbale.setdefault("rapporti", [])
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.resize(1000, 600)
        self.build_left_panel()
        self.build_right_panel()
        self.setStyleSheet("background-color: gray; color: white;")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)

    def build_left_panel(self):
        left_panel = QVBoxLayout()
        header_layout = QHBoxLayout()

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

        titolo = QLabel("Rapporti disciplinari:")
        titolo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titolo.setStyleSheet("color: white;")

        header_layout.addWidget(back_btn)
        header_layout.addWidget(titolo)
        header_layout.addStretch()
        left_panel.addLayout(header_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(12)

        # Mostra solo i rapporti del verbale aperto
        for rapporto in self.rapporti_disciplinari:
            box = QFrame()
            box.setFixedHeight(150)
            box.setStyleSheet("background-color: white; border-radius: 15px;")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(10, 10, 10, 10)

            header_layout_box = QHBoxLayout()
            agente_icon = QLabel()
            agente_icon.setPixmap(QPixmap(":/Images/Images/user.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
            agente_label = QLabel(rapporto['agente'])
            agente_label.setStyleSheet("color: black; font-weight: bold;")

            data_icon = QLabel()
            data_icon.setPixmap(QPixmap(":/Images/Images/calendar.png").scaled(18, 18, Qt.AspectRatioMode.KeepAspectRatio))
            data_label = QLabel(rapporto['data'])
            data_label.setStyleSheet("color: black;")

            header_layout_box.addWidget(agente_icon)
            header_layout_box.addWidget(agente_label)
            header_layout_box.addStretch()
            header_layout_box.addWidget(data_icon)
            header_layout_box.addWidget(data_label)

            testo = QLabel(rapporto["testo"])
            testo.setWordWrap(True)
            testo.setStyleSheet("color: black;")
    
            # Layout verticale per il fondo del box
            bottom_container = QVBoxLayout()
            bottom_container.addStretch()
            
            bottom_layout = QHBoxLayout()

            apri_btn = QPushButton("Apri rapporto")
            apri_btn.setStyleSheet("background-color: #666; color: white; padding: 6px; border-radius: 8px;")
            apri_btn.setFixedSize(100, 30) 
            apri_btn.clicked.connect(lambda _, r=rapporto: self.apri_rapporto(r))
            bottom_layout.addWidget(apri_btn)
            
            # Bottone modifica rapporto
            modifica_btn = QPushButton()
            modifica_btn.setIcon(QIcon(":/Images/Images/modifica.png"))
            modifica_btn.setFixedSize(30, 30)
            modifica_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ddd;
                    border-radius: 5px;
                }
            """)
            modifica_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            modifica_btn.clicked.connect(lambda _, r=rapporto: self.modifica_rapporto(r))
            bottom_layout.addWidget(modifica_btn, alignment=Qt.AlignmentFlag.AlignRight)
            
            bottom_container.addLayout(bottom_layout)

            # Fusione del tutto
            box_layout.addLayout(header_layout_box)
            box_layout.addWidget(testo)
            box_layout.addLayout(bottom_container)
            
            scroll_layout.addWidget(box)

        scroll_area.setWidget(scroll_content)
        left_panel.addWidget(scroll_area)

        if hasattr(self, "left_widget"):
            self.main_layout.removeWidget(self.left_widget)
            self.left_widget.deleteLater()

        self.left_widget = QWidget()
        self.left_widget.setLayout(left_panel)
        self.main_layout.insertWidget(0, self.left_widget)

    def build_right_panel(self):
        right_panel = QVBoxLayout()
        aggiungi_btn = QPushButton(" Aggiungi Rapporto")
        aggiungi_btn.setIcon(QIcon(":/Images/Images/nuovoV.png"))
        aggiungi_btn.setIconSize(QSize(18, 18))
        aggiungi_btn.setFixedSize(150, 40)
        aggiungi_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 12px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ddd;
            }
        """)
        aggiungi_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        aggiungi_btn.clicked.connect(self.apri_aggiungi_rapporto)

        right_panel.addWidget(aggiungi_btn, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        right_panel.addStretch()

        self.right_widget = QWidget()
        self.right_widget.setLayout(right_panel)
        self.main_layout.addWidget(self.right_widget)

        crest = QLabel()
        crest.setPixmap(QPixmap(":/Images/Images/logo.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        right_panel.addStretch()
        right_panel.addWidget(crest, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

    # Metodi
    def apri_aggiungi_rapporto(self):
        self.hide()
        # Aggiungi rapporto SOLO al verbale corrente
        self.aggiungi_window = AggiungiRapportoWindow(self)
        self.aggiungi_window.show()

    def apri_rapporto(self, rapporto):
        dlg = RapportoDialog(rapporto, self)
        dlg.exec()

    def aggiorna(self):
        self.build_left_panel()
        self.show()
        
    def modifica_rapporto(self, rapporto):
        dlg = ModificaRapportoDialog(rapporto, self)
        dlg.exec()
        # Dopo la modifica aggiorno la UI
        self.build_left_panel()


# Classe per far leggere tutto il rapporto            
class RapportoDialog(QDialog):
    def __init__(self, rapporto, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rapporto disciplinare")
        self.resize(600, 400)
        self.setStyleSheet("background-color: gray; color: white;")

        layout = QVBoxLayout(self)
        
        titolo = QLabel(f"Agente: {rapporto['agente']} - Data: {rapporto['data']}")
        titolo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        titolo.setStyleSheet("color: white;")
        layout.addWidget(titolo)

        testo = QTextEdit()
        testo.setReadOnly(True)
        testo.setText(rapporto["testo"])
        testo.setStyleSheet("background-color: white; color: black; font-size: 14px;")
        layout.addWidget(testo)

        chiudi_btn = QPushButton("Chiudi")
        chiudi_btn.setStyleSheet("background-color: #444; color: white; padding: 6px;")
        chiudi_btn.clicked.connect(self.close)
        layout.addWidget(chiudi_btn, alignment=Qt.AlignmentFlag.AlignRight)

class ModificaRapportoDialog(QDialog):
    def __init__(self, rapporto, parent=None):
        super().__init__(parent)
        self.rapporto = rapporto
        self.setWindowTitle("Modifica Rapporto")
        self.resize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        titolo = QLabel("Modifica testo del rapporto")
        titolo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(titolo)

        # Campo di testo
        self.text_edit = QTextEdit()
        self.text_edit.setText(self.rapporto["testo"])
        layout.addWidget(self.text_edit)

        # Bottone salva e annulla
        btn_layout = QHBoxLayout()
        
        salva_btn = QPushButton("Salva")
        salva_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        salva_btn.clicked.connect(self.salva_modifica)
        btn_layout.addWidget(salva_btn)
        
        annulla_btn = QPushButton("Annulla")
        annulla_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        annulla_btn.clicked.connect(self.reject)
        btn_layout.addWidget(annulla_btn)
        
        layout.addLayout(btn_layout)

    def salva_modifica(self):
        # Aggiorna il testo del rapporto
        self.rapporto["testo"] = self.text_edit.toPlainText()
        self.accept()