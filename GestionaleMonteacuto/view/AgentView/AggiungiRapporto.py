from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont


class AggiungiRapportoWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.setWindowTitle("Aggiungi Rapporto")
        self.resize(600, 400)
        self.setStyleSheet("background-color: gray; color: white;")

        # Riferimento a VisualizzaVerbaleWindow
        self.parent_window = parent_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        titolo = QLabel("Nuovo Rapporto Disciplinare")
        titolo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titolo)

        # Nome agente
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome Agente")
        layout.addWidget(self.nome_input)

        # Data
        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())
        layout.addWidget(self.data_input)

        # Testo rapporto
        self.testo_input = QTextEdit()
        self.testo_input.setPlaceholderText("Scrivi qui il rapporto...")
        layout.addWidget(self.testo_input)

        # Pulsanti salva e annulla
        btn_layout = QHBoxLayout()

        salva_btn = QPushButton("Salva")
        salva_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        salva_btn.clicked.connect(self.salva_rapporto)
        btn_layout.addWidget(salva_btn)

        annulla_btn = QPushButton("Annulla")
        annulla_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        annulla_btn.clicked.connect(self.annulla)
        btn_layout.addWidget(annulla_btn)

        layout.addLayout(btn_layout)

    # Metdodo per il bottone salva
    def salva_rapporto(self):
        nuovo_rapporto = {
            "agente": self.nome_input.text(),
            "data": self.data_input.date().toString("dd/MM/yyyy"),
            "testo": self.testo_input.toPlainText()
        }

        # Aggiungi il rapporto alla lista della finestra principale
        self.parent_window.rapporti_disciplinari.append(nuovo_rapporto)
        self.parent_window.aggiorna()
        self.close()

        # Torna alla finestra principale
        self.close()
        self.parent_window.show()

    # Metodo per il bottone annulla
    def annulla(self):
        # Torna alla finestra principale senza salvare
        self.close()
        self.parent_window.show()