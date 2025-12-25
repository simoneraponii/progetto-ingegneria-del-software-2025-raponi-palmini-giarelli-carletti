import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class ModificaUtente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modifica utente")
        self.setFixedSize(900, 550)
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
            }

            QGroupBox {
                background: #f4f4f4;
                border-radius: 18px;
                font-size: 18px;
                font-weight: bold;
                padding-top: 25px;
            }

            QLineEdit, QTextEdit {
                background: white;
                border: 2px solid #cccccc;
                border-radius: 12px;
                padding: 6px 10px;
                font-size: 14px;
            }

            QPushButton {
                background: #ffffff;
                border: 2px solid #cdcdcd;
                border-radius: 12px;
                padding: 6px;
            }

            QPushButton:hover {
                background: #e6e6e6;
            }
        """)

        layout = QVBoxLayout(self)

        # Titolo
        titolo = QLabel("Modifica utente")
        titolo.setStyleSheet("color: white; font-size: 22px; font-weight: bold; margin-left: 10px;")
        layout.addWidget(titolo)

        # Box centrale
        box = QGroupBox("Profilo")
        box_layout = QVBoxLayout()
        box.setLayout(box_layout)
        box.setMinimumHeight(350)

        # Prima riga: Nome - Cognome - Data di nascita
        riga1 = QHBoxLayout()

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")

        self.cognome = QLineEdit()
        self.cognome.setPlaceholderText("Cognome")
        self.dn = QLineEdit()
        self.dn.setPlaceholderText("gg/mm/yyyy")

        riga1.addWidget(self.nome)
        riga1.addWidget(self.cognome)
        riga1.addWidget(self.dn)

        # Seconda riga: Luogo nascita - Username - Password
        riga2 = QHBoxLayout()

        self.luogo = QLineEdit()
        self.luogo.setPlaceholderText("Luogo di nascita")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        riga2.addWidget(self.luogo)
        riga2.addWidget(self.username)
        riga2.addWidget(self.password)

        # Terza riga: Stato account - Ruolo
        riga3 = QHBoxLayout()

        self.stato = QLineEdit()
        self.stato.setPlaceholderText("Account: attivo")

        self.ruolo = QLineEdit()
        self.ruolo.setPlaceholderText("Ruolo")

        riga3.addWidget(self.stato)
        riga3.addWidget(self.ruolo)

        # Box note
        self.note = QTextEdit()
        self.note.setPlaceholderText("Note aggiuntive...")

        # Pulsanti
        riga_bottoni = QHBoxLayout()
        riga_bottoni.addStretch()

        btn_salva = QPushButton()
        btn_salva.setIcon(QIcon.fromTheme("document-save"))

        btn_annulla = QPushButton()
        btn_annulla.setIcon(QIcon.fromTheme("window-close"))

        riga_bottoni.addWidget(btn_salva)
        riga_bottoni.addWidget(btn_annulla)

        # Assemblaggio layout
        box_layout.addLayout(riga1)
        box_layout.addLayout(riga2)
        box_layout.addLayout(riga3)
        box_layout.addWidget(self.note)
        box_layout.addLayout(riga_bottoni)

        layout.addWidget(box)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ModificaUtente()
    w.show()
    sys.exit(app.exec())
