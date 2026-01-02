import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QLineEdit, QTextEdit, QDateEdit, QGridLayout, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate

from app.session import Session
from controller.detenuti_controller import DetenutiController

class NuovoDetenutoView(QWidget):
    def __init__(self,session:Session):
        super().__init__()
        self.setWindowTitle("Nuovo Detenuto")
        self.detenuti_controller = DetenutiController()
        self.session = session
        self.resize(900, 700)
        self.setMinimumSize(700, 500)
        # --- STILE GENERALE ---
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F9;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QScrollArea {
                border: none;
                background-color: #F4F6F9;
            }
            QScrollBar:vertical {
                border: none;
                background: #E0E0E0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #A0A0A0;
                min-height: 20px;
                border-radius: 5px;
            }
        """)

        self.window_layout = QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)

        self.setup_ui()

    def setup_ui(self):
        # --- HEADER ---
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background-color: #FFFFFF;
            border-bottom: 1px solid #E0E0E0;
        """)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        title_label = QLabel("Nuova Registrazione")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2C3E50; border: none; background: transparent;")

        h_layout.addWidget(title_label)
        h_layout.addStretch()
        self.window_layout.addWidget(header)

        # --- SCROLL AREA ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        form_container = QWidget()
        form_container.setStyleSheet("background-color: #F4F6F9;")
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(30, 20, 30, 30)
        form_layout.setSpacing(20)

        # --- DATI ANAGRAFICI ---
        self.add_section_title(form_layout, "DATI ANAGRAFICI")
        anagrafica_card = self.create_card()
        grid_a = QGridLayout(anagrafica_card)
        grid_a.setSpacing(15)
        grid_a.setContentsMargins(20, 20, 20, 20)

        self.input_nome = self.add_field(grid_a, "Nome", 0, 0)
        self.input_cognome = self.add_field(grid_a, "Cognome", 0, 1)
        self.input_luogo_nascita = self.add_field(grid_a, "Luogo di Nascita", 0, 2)

        self.input_cf = self.add_field(grid_a, "Codice Fiscale", 1, 0)
        self.input_data_nascita = self.add_date_field(grid_a, "Data di Nascita", 1, 1)
        self.input_matricola = self.add_field(grid_a, "Matricola", 1, 2)

        # --- DETENZIONE E UBICAZIONE ---
        self.add_section_title(form_layout, "DETENZIONE E UBICAZIONE")
        ubicazione_card = self.create_card()
        grid_b = QGridLayout(ubicazione_card)
        grid_b.setSpacing(15)
        grid_b.setContentsMargins(20, 20, 20, 20)

        self.input_sezione = self.add_field(grid_b, "Sezione", 0, 0)
        self.input_camera = self.add_field(grid_b, "Camera", 0, 1)
        self.input_fine_pena = self.add_date_field(grid_b, "Fine Pena", 0, 2)

        # --- CAPI D'ACCUSA ---
        self.add_section_title(form_layout, "CAPI D'ACCUSA")
        accuse_card = self.create_card()
        v_accuse = QVBoxLayout(accuse_card)
        v_accuse.setContentsMargins(20, 20, 20, 20)

        self.text_accuse = QTextEdit()
        self.text_accuse.setMinimumHeight(100)
        self.text_accuse.setPlaceholderText("Inserire i reati o le note relative alla detenzione...")
        self.text_accuse.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                color: #333333;
                padding: 8px;
            }
            QTextEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        v_accuse.addWidget(self.text_accuse)

        form_layout.addWidget(anagrafica_card)
        form_layout.addWidget(ubicazione_card)
        form_layout.addWidget(accuse_card)

        # --- BOTTONI ---
        actions = QHBoxLayout()
        actions.setContentsMargins(0, 10, 0, 0)

        self.btn_save = QPushButton("SALVA REGISTRAZIONE")
        self.btn_save.setFixedSize(200, 45)
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover { background-color: #005a9e; }
            QPushButton:pressed { background-color: #004578; }
        """)

        actions.addStretch()
        actions.addWidget(self.btn_save)
        form_layout.addLayout(actions)

        scroll.setWidget(form_container)
        self.window_layout.addWidget(scroll)

        self.btn_save.clicked.connect(self.on_salva_click)

    # --- METODI AUSILIARI ---
    def add_section_title(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #5F6368; font-weight: bold; font-size: 12px; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(lbl)

    def create_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #DCE1E7;
                border-radius: 8px;
            }
        """)
        return card

    def add_field(self, layout, label_text, row, col):
        vbox = QVBoxLayout()
        vbox.setSpacing(6)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: #444; font-weight: 600; font-size: 13px;")

        field = QLineEdit()
        field.setFixedHeight(35)
        field.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                color: #333333;
                padding-left: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078D4;
            }
        """)

        vbox.addWidget(lbl)
        vbox.addWidget(field)
        layout.addLayout(vbox, row, col)
        return field

    def add_date_field(self, layout, label_text, row, col):
        vbox = QVBoxLayout()
        vbox.setSpacing(6)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: #444; font-weight: 600; font-size: 13px;")

        date_inp = QDateEdit()
        date_inp.setCalendarPopup(True)
        date_inp.setDate(QDate.currentDate())
        date_inp.setDisplayFormat("dd/MM/yyyy")
        date_inp.setFixedHeight(35)
        date_inp.setStyleSheet("""
            QDateEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                color: #333333;
                padding-left: 10px;
            }
            QDateEdit:focus {
                border: 1px solid #0078D4;
            }
            QDateEdit::drop-down {
                width: 25px;
                border-left: 1px solid #CCCCCC;
                background-color: #F9F9F9;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QDateEdit::down-arrow {
                image: none;
                width: 0; height: 0;
            }
        """)

        vbox.addWidget(lbl)
        vbox.addWidget(date_inp)
        layout.addLayout(vbox, row, col)
        return date_inp

    def on_salva_click(self):
        dati_detenuto = {
            "datoAnagrafico": {
                "codiceFiscale": str(self.input_cf.text()).strip().upper(),
                "nome": str(self.input_nome.text()).strip(),
                "cognome": str(self.input_cognome.text()).strip(),
                "dataNascita": self.input_data_nascita.date().toString("yyyy-MM-dd"),
                "luogoNascita": str(self.input_luogo_nascita.text()).strip()
            },
            "pena": {
                "descrizione": str(self.text_accuse.toPlainText()).strip(),
                "dataFinePena": self.input_fine_pena.date().toString("yyyy-MM-dd")
            },
            "ubicazione": {
                "sezione": str(self.input_sezione.text()).strip(),
                "cella": str(self.input_camera.text()).strip()
            },
            "detenuto": {
                "matricola": str(self.input_matricola.text()).strip()
            }
        }

        if not dati_detenuto["detenuto"]["matricola"]:
            QMessageBox.warning(self, "Campo Mancante", "Il campo Matricola obbligatorio.")
            return

        try:
            if self.detenuti_controller.crea_nuovo_detenuto(dati_detenuto):
                QMessageBox.information(self, "Successo", "Detenuto registrato con successo!")
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Errore durante il salvataggio nel database.")
        except Exception as e:
            QMessageBox.critical(self, "Errore Fatale", f"Errore di sistema: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NuovoDetenutoView()
    window.show()
    sys.exit(app.exec())
