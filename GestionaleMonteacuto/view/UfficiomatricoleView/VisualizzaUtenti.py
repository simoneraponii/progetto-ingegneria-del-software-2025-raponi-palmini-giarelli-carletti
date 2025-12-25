import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QLineEdit, QScrollArea
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class VisualizzaUtenti(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualizza utente")
        self.setGeometry(150, 80, 1300, 750)
        self.setStyleSheet("background-color: black;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # BARRA SUPERIORE
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background-color: #e6e6e6;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        left_section = QHBoxLayout()
        user_icon = QLabel("👤")
        user_icon.setFont(QFont("Arial", 18))
        left_section.addWidget(user_icon)

        name_label = QLabel("Nome Cognome")
        name_label.setFont(QFont("Arial", 12))
        name_label.setStyleSheet("color: #777;")
        left_section.addWidget(name_label)

        left_container = QWidget()
        left_container.setLayout(left_section)
        left_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_layout.addWidget(left_container)

        title = QLabel("Benvenuto Ufficio Matricole!")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #555;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        center_container = QWidget()
        cc = QHBoxLayout(center_container)
        cc.addWidget(title)
        center_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_layout.addWidget(center_container)

        right_container = QWidget()
        right_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_layout.addWidget(right_container)

        main_layout.addWidget(top_bar)

        # CONTENUTO CENTRALE
        central = QFrame()
        central.setStyleSheet("background-color: #c1c1c1;")
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(20, 10, 20, 20)
        central_layout.setSpacing(15)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(20)

        back_button = QPushButton("↩")
        back_button.setFixedSize(60, 60)
        back_button.setFont(QFont("Arial", 24))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 30px;
                border: 1px solid #ccc;
            }
            QPushButton:hover { background-color: #f2f2f2; }
        """)
        top_row.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        top_row.addStretch(1)

        section_title = QLabel("Visualizza utenti")
        section_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #444;")
        top_row.addWidget(section_title, alignment=Qt.AlignmentFlag.AlignCenter)

        top_row.addStretch(1)

        new_user_btn = QPushButton("👤➕  Nuovo Utente")
        new_user_btn.setFixedSize(180, 45)
        new_user_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #bbb;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #f3f3f3; }
        """)
        top_row.addWidget(new_user_btn, alignment=Qt.AlignmentFlag.AlignRight)

        central_layout.addLayout(top_row)

        # SEARCH BAR
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
            padding: 8px;
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 5, 15, 5)

        icon = QLabel("👥")
        icon.setFont(QFont("Arial", 18))
        search_layout.addWidget(icon)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Inserisci il nome dell’utente...")
        search_bar.setFont(QFont("Arial", 14))
        search_bar.setStyleSheet("border: none;")
        search_layout.addWidget(search_bar)

        search_button = QPushButton("🔍")
        search_button.setFont(QFont("Arial", 18))
        search_button.setFixedSize(40, 40)
        search_button.setStyleSheet("border: none;")
        search_layout.addWidget(search_button)

        central_layout.addWidget(search_frame)

        # SCROLL AREA LISTA UTENTI
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(12)

        for _ in range(8):
            row = QFrame()
            row.setStyleSheet("background: white; border-radius: 15px;")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(15, 10, 15, 10)
            row_layout.setSpacing(20)

            for label in ("Nome", "Cognome"):
                field = QLineEdit()
                field.setPlaceholderText(label)
                field.setReadOnly(True)
                field.setFixedHeight(35)
                field.setStyleSheet("""
                    background: #f7f7f7;
                    border: 1px solid #bbb;
                    border-radius: 15px;
                    padding-left: 10px;
                """)
                row_layout.addWidget(field)

            stato_label = QLineEdit()
            stato_label.setPlaceholderText("Account: attivo")
            stato_label.setReadOnly(True)
            stato_label.setFixedHeight(35)
            stato_label.setStyleSheet("""
                background: #f7f7f7;
                border: 1px solid #bbb;
                border-radius: 15px;
                padding-left: 10px;
            """)
            row_layout.addWidget(stato_label)

            view_btn = QPushButton("🔍 Visualizza utente")
            view_btn.setFixedHeight(35)
            view_btn.setStyleSheet("""
                background: #dedede;
                border-radius: 15px;
            """)
            row_layout.addWidget(view_btn)

            scroll_layout.addWidget(row)

        scroll.setWidget(scroll_content)
        central_layout.addWidget(scroll)

        # LOGO FINALE
        bottom_logo = QLabel()
        try:
            pix = QPixmap("logo.png").scaled(
                150, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            bottom_logo.setPixmap(pix)
        except:
            bottom_logo.setText("[Logo]")

        central_layout.addWidget(bottom_logo, alignment=Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(central)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VisualizzaUtenti()
    sys.exit(app.exec())
