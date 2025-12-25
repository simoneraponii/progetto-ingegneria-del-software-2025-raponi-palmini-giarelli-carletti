import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt

class ConfermaInserimento(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggiungi Detenuto")
        self.setFixedSize(900, 550)

        # Sfondo scuro senza sfocature
        self.setStyleSheet("""
            QWidget {
                background-color: #303030;
            }

            QFrame#dialogBox {
                background: #ffffff;
                border-radius: 24px;
            }

            QLabel#domanda {
                font-size: 16px;
                color: #000000;
            }

            QPushButton#btnSi {
                background-color: #000000;
                color: #ffffff;
                border-radius: 14px;
                padding: 6px 20px;
                font-size: 14px;
            }
            QPushButton#btnSi:hover {
                background-color: #222222;
            }

            QPushButton#btnNo {
                background-color: #e0e0e0;
                color: #000000;
                border-radius: 14px;
                padding: 6px 20px;
                font-size: 14px;
            }
            QPushButton#btnNo:hover {
                background-color: #d0d0d0;
            }
        """)

        layout = QVBoxLayout(self)

        # --- Dialog box centrale ---
        dialog = QFrame()
        dialog.setObjectName("dialogBox")
        dialog.setFixedSize(330, 170)

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(25, 20, 25, 20)
        dialog_layout.setSpacing(18)

        # Testo domanda
        domanda = QLabel("Desideri confermare l'inserimento\n del nuovo detenuto?")
        domanda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        domanda.setObjectName("domanda")
        dialog_layout.addWidget(domanda)

        # Pulsanti
        bottoni_layout = QHBoxLayout()

        btn_si = QPushButton("Si")
        btn_si.setObjectName("btnSi")

        btn_no = QPushButton("No")
        btn_no.setObjectName("btnNo")

        bottoni_layout.addWidget(btn_si)
        bottoni_layout.addWidget(btn_no)

        dialog_layout.addLayout(bottoni_layout)

        # Layout principale → centra la finestra
        layout.addStretch()
        cent = QHBoxLayout()
        cent.addStretch()
        cent.addWidget(dialog)
        cent.addStretch()
        layout.addLayout(cent)
        layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ConfermaInserimento()
    w.show()
    sys.exit(app.exec())
