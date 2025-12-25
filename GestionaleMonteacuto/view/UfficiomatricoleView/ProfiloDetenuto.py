import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QLineEdit, QTextEdit, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


class ProfiloDetenuto(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Profilo detenuto")
        self.setGeometry(200, 100, 1200, 700)
        self.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------------

        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background-color: #D9D9D9;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 0, 0)

        title = QLabel("Profilo detenuto")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #555;")
        top_layout.addWidget(title)

        main_layout.addWidget(top_bar)

        # ----------------------------------------------------------
        # MIDDLE AREA (background + content)
        # ----------------------------------------------------------

        middle = QFrame()
        middle.setStyleSheet("background-color: #bfbfbf;")
        middle_layout = QVBoxLayout(middle)
        middle_layout.setContentsMargins(30, 20, 30, 20)

        # Freccia indietro
        back_btn = QPushButton("↩")
        back_btn.setFont(QFont("Arial", 22))
        back_btn.setFixedSize(55, 55)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 27px;
                border: 1px solid #aaa;
            }
        """)
        middle_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # ----------------------------------------------------------
        # WHITE CARD (container)
        # ----------------------------------------------------------

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 25, 40, 25)
        card_layout.setSpacing(20)

        # TITLE "Profilo"
        profile_title = QLabel("Profilo")
        profile_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        profile_title.setStyleSheet("color: #444;")
        profile_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(profile_title)

        # ----------------------------------------------------------
        # FIRST ROW (Nome, Cognome, Matricola)
        # ----------------------------------------------------------

        row1 = QHBoxLayout()
        row1.setSpacing(25)

        def create_lineEdit(ph):
            le = QLineEdit()
            le.setPlaceholderText(ph)
            le.setFixedHeight(35)
            le.setStyleSheet("""
                QLineEdit {
                    background-color: #f7f7f7;
                    border: 1px solid #bbb;
                    border-radius: 15px;
                    padding-left: 10px;
                }
            """)
            return le

        nome = create_lineEdit("👤  Nome")
        cognome = create_lineEdit("👥  Cognome")
        matricola = create_lineEdit("🪪  Matricola")

        row1.addWidget(nome)
        row1.addWidget(cognome)
        row1.addWidget(matricola)

        card_layout.addLayout(row1)

        # ----------------------------------------------------------
        # SECOND COLUMN (Codice fiscale, data nascita, fine pena)
        # ----------------------------------------------------------

        col_area = QHBoxLayout()
        col_area.setSpacing(30)

        left_col = QVBoxLayout()
        left_col.setSpacing(15)

        cf = create_lineEdit("👤  Codice Fiscale")
        dnascita = create_lineEdit("📅  Data di nascita")
        dfpena = create_lineEdit("⏳  Data fine pena")

        left_col.addWidget(cf)
        left_col.addWidget(dnascita)
        left_col.addWidget(dfpena)

        # Right text area (Accuse)
        accuse = QTextEdit()
        accuse.setPlaceholderText("Accuse...")
        accuse.setFixedHeight(200)
        accuse.setStyleSheet("""
            QTextEdit {
                background-color: #f7f7f7;
                border: 1px solid #bbb;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        col_area.addLayout(left_col)
        col_area.addWidget(accuse)

        card_layout.addLayout(col_area)

        # ----------------------------------------------------------
        # BOTTOM BUTTON
        # ----------------------------------------------------------

        btn_modifica = QPushButton("📝  Modifica detenuto")
        btn_modifica.setFixedSize(200, 45)
        btn_modifica.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #777;
                border-radius: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        card_layout.addWidget(btn_modifica, alignment=Qt.AlignmentFlag.AlignRight)

        # Add card to center
        middle_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        # ----------------------------------------------------------
        # LOGO AREA
        # ----------------------------------------------------------

        logo = QLabel()
        try:
            pix = QPixmap("logo.png").scaled(
                160, 170,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo.setPixmap(pix)
        except:
            logo.setText("[Logo]")

        middle_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(middle)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfiloDetenuto()
    sys.exit(app.exec())
