import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class ConfermaLogout(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logout")
        self.setFixedSize(900, 550)

        # Manteniamo lo sfondo scuro
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

        # Dialog box bianco in primo piano
        dialog = QFrame()
        dialog.setObjectName("dialogBox")
        dialog.setFixedSize(330, 170)
        dialog.setStyleSheet("QFrame#dialogBox { z-index: 10; }")  # forza primo piano

        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(25, 20, 25, 20)
        dialog_layout.setSpacing(18)

        # Scritta con ombra leggera
        domanda = QLabel("Desideri confermare il logout?")
        domanda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        domanda.setObjectName("domanda")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(60, 60, 60, 100))  # ombra morbida e trasparente
        domanda.setGraphicsEffect(shadow)

        dialog_layout.addWidget(domanda)

        # Pulsanti
        bottoni_layout = QHBoxLayout()

        btn_si = QPushButton("Sì")
        btn_si.setObjectName("btnSi")
        btn_si.clicked.connect(self.conferma_logout)

        btn_no = QPushButton("No")
        btn_no.setObjectName("btnNo")
        btn_no.clicked.connect(self.annulla_logout)

        bottoni_layout.addWidget(btn_si)
        bottoni_layout.addWidget(btn_no)

        dialog_layout.addLayout(bottoni_layout)

        # Centra il box bianco
        layout.addStretch()
        cent = QHBoxLayout()
        cent.addStretch()
        cent.addWidget(dialog)
        cent.addStretch()
        layout.addLayout(cent)
        layout.addStretch()

    def conferma_logout(self):
        QApplication.quit()

    def annulla_logout(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ConfermaLogout()
    w.show()
    sys.exit(app.exec())
