import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QScrollArea,
    QSizePolicy, QMessageBox, QApplication
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
from PyQt6.QtCore import Qt
from view.AgentView import resources_rc
from view.AgentView.VisualizzaDetenuto import VisualizzaDetenutoWindow
from controller.detenuti_controller import DetenutiController
from model.DTO.detenuto_dto import DetenutoDTO
from app.session import Session


class AgentDashboardWindow(QWidget):
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)

        self.session = session
        self.detenuto_controller = DetenutiController()

        # Nome utente formattato
        self.agente_nome = f"{session.current_user.ruolo} {session.current_user.cognome}"

        self.setWindowTitle("Dashboard Agente")
        self.setGeometry(100, 100, 1200, 700) # Dimensioni simili al tuo esempio
        
        # 1. SFONDO NERO GENERALE
        self.setStyleSheet("background-color: black;")

        # Caricamento dati
        self.detainees = self.load_detenuti()

        self.init_ui()

    # ==========================================
    # LOGICA CARICAMENTO DATI
    # ==========================================
    def load_detenuti(self) -> list[DetenutoDTO]:
        try:
            detenuti = self.detenuto_controller.getDetenutiDto()
            # Ordinamento alfabetico per Cognome, poi Nome
            return sorted(
                detenuti,
                key=lambda d: (d.cognome.lower(), d.nome.lower(), d.matricola.lower())
            )
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare i detenuti:\n{e}")
            return []

    # ==========================================
    # INTERFACCIA UTENTE
    # ==========================================
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --------------------------------------
        # BARRA SUPERIORE (Grigio Chiaro)
        # --------------------------------------
        top_bar = QFrame()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #e6e6e6;")
        
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 10, 20, 10)

        # SINISTRA: Icona Utente + Nome Agente
        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0,0,0,0)
        
        user_icon = QLabel()
        user_icon.setPixmap(QPixmap(":/Images/Images/agente.png").scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio))
        
        name_label = QLabel(self.agente_nome)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #333;")
        
        left_layout.addWidget(user_icon)
        left_layout.addWidget(name_label)
        
        # CENTRO: Titolo Benvenuto
        title_label = QLabel("Dashboard Operativa")
        title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #555;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DESTRA: Pulsante Logout
        logout_btn = QPushButton(" Logout")
        logout_btn.setIcon(QIcon(":/Images/Images/logout.png"))
        logout_btn.setFixedSize(110, 40)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #bbb;
                border-radius: 10px;
                color: #333;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ffdddd; border-color: red; }
        """)
        logout_btn.clicked.connect(self.logout)

        # Assemblaggio Top Bar
        top_layout.addWidget(left_container, stretch=1)
        top_layout.addWidget(title_label, stretch=2)
        top_layout.addWidget(logout_btn, stretch=1, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(top_bar)

        # --------------------------------------
        # AREA CENTRALE (Grigio Scuro)
        # --------------------------------------
        central_frame = QFrame()
        central_frame.setStyleSheet("background-color: #c1c1c1;")
        
        central_layout = QVBoxLayout(central_frame)
        central_layout.setContentsMargins(30, 20, 30, 20)
        central_layout.setSpacing(15)

        # -- Intestazione Sezione --
        header_row = QHBoxLayout()
        
        section_title = QLabel("Lista Detenuti Presenti")
        section_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #444;")
        

        header_row.addStretch()
        header_row.addWidget(section_title)
        header_row.addStretch()
        
        central_layout.addLayout(header_row)


        search_frame = QFrame()
        search_frame.setFixedHeight(60)
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 5, 15, 5)

        icon_lens = QLabel("🔍")
        icon_lens.setFont(QFont("Arial", 16))
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cerca per Cognome, Nome o Matricola...")
        self.search_bar.setFont(QFont("Arial", 14))
        self.search_bar.setStyleSheet("border: none; background: transparent;")
        self.search_bar.textChanged.connect(self.filter_list)
        
        search_layout.addWidget(icon_lens)
        search_layout.addWidget(self.search_bar)

        central_layout.addWidget(search_frame)

        # -- Scroll Area (Lista) --
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #c1c1c1;") # Sfondo uguale al frame
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(0, 10, 0, 10)

        # Popolamento Iniziale
        self.populate_list(self.detainees)

        self.scroll_area.setWidget(self.scroll_content)
        central_layout.addWidget(self.scroll_area)

        # -- Logo in basso a destra --
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        
        logo_label = QLabel()
        logo_pix = QPixmap(":/Images/Images/logo.png")
        if not logo_pix.isNull():
            logo_label.setPixmap(logo_pix.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        bottom_row.addWidget(logo_label)
        central_layout.addLayout(bottom_row)

        main_layout.addWidget(central_frame)

    # ==========================================
    # METODI DI POPOLAMENTO LISTA
    # ==========================================
    def populate_list(self, data_list: list[DetenutoDTO]):
        # Pulisci lista
        for i in reversed(range(self.scroll_layout.count())):
            w = self.scroll_layout.itemAt(i).widget()
            if w:
                w.deleteLater()

        if not data_list:
            lbl = QLabel("Nessun detenuto trovato.")
            lbl.setFont(QFont("Arial", 14))
            lbl.setStyleSheet("color: #555;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scroll_layout.addWidget(lbl)
            return

        # Genera righe
        for det in data_list:
            row_frame = QFrame()
            row_frame.setFixedHeight(70)
            row_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 15px;
                }
            """)
            
            row_layout = QHBoxLayout(row_frame)
            row_layout.setContentsMargins(15, 10, 15, 10)
            row_layout.setSpacing(15)

            input_style = """
                QLineEdit {
                    background: #f7f7f7;
                    border: 1px solid #bbb;
                    border-radius: 10px;
                    padding-left: 10px;
                    color: black;
                    font-size: 14px;
                }
            """

            # 1. Cognome
            edt_cognome = QLineEdit(det.cognome)
            edt_cognome.setReadOnly(True)
            edt_cognome.setPlaceholderText("Cognome")
            edt_cognome.setStyleSheet(input_style)
            
            # 2. Nome
            edt_nome = QLineEdit(det.nome)
            edt_nome.setReadOnly(True)
            edt_nome.setPlaceholderText("Nome")
            edt_nome.setStyleSheet(input_style)

            # 3. Matricola
            edt_matr = QLineEdit(det.matricola)
            edt_matr.setReadOnly(True)
            edt_matr.setPlaceholderText("Matricola")
            edt_matr.setStyleSheet(input_style)
            edt_matr.setFixedWidth(120) # La matricola è più corta

            # 4. Bottone Visualizza
            btn_view = QPushButton("Visualizza")
            btn_view.setFixedSize(100, 40)
            btn_view.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_view.setStyleSheet("""
                QPushButton {
                    background-color: #dedede;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #cccccc;
                }
            """)
            # Connessione segnale
            btn_view.clicked.connect(lambda checked, d=det: self.apri_detenuto(d))

            # Aggiunta al layout riga
            row_layout.addWidget(edt_cognome, stretch=2)
            row_layout.addWidget(edt_nome, stretch=2)
            row_layout.addWidget(edt_matr, stretch=1)
            row_layout.addWidget(btn_view)

            self.scroll_layout.addWidget(row_frame)

        # Spacer finale per spingere tutto in alto
        self.scroll_layout.addStretch()

    # ==========================================
    # LOGICA FUNZIONALE
    # ==========================================
    def filter_list(self):
        testo = self.search_bar.text().lower().strip()
        
        filtrati = [
            d for d in self.detainees
            if testo in d.cognome.lower() 
            or testo in d.nome.lower() 
            or testo in d.matricola.lower()
        ]
        self.populate_list(filtrati)

    def apri_detenuto(self, det: DetenutoDTO):
        self.detenuto_window = VisualizzaDetenutoWindow(self.session, det.matricola)
        self.detenuto_window.show()

    def logout(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Logout")
        msg_box.setText("Sei sicuro di voler uscire?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No) 
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                border: 1px solid #ccc;
            }
            QLabel {
                color: black;
                font-family: Arial;
                font-size: 14px;
                background-color: transparent; 
            }
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #bbb;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 13px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
                border-color: #999;
            }
            QPushButton:pressed {
                background-color: #d4d4d4;
            }
        """)

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            self.session.current_user = None
            self.close()
            from view.LoginView.login_view import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()