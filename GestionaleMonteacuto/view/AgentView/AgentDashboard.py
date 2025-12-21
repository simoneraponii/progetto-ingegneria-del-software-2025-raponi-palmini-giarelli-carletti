from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QPalette, QColor
from PyQt6.QtCore import Qt
from view.AgentView import resources_rc
import sys
from view.AgentView.VisualizzaDetenuto import VisualizzaDetenutoWindow
from app.session import Session

class AgentDashboardWindow(QWidget):
    
    def __init__(self, session:Session):
        super().__init__()
        self.agente_nome = f"{session.current_user.ruolo.value} {session.current_user.cognome}"
        self.setWindowTitle("Dashboard Agente")
        self.resize(1000, 600)
        self.detainees = self.get_detainees()
        self.setStyleSheet("background-color: light gray;")
        self.init_ui()

    def get_detainees(self):
        return [
            ("Gabriel", "Popa", "D001"),
            ("Luigi", "Verdi", "D002"),
            ("Anna", "Bianchi", "D003"),
            ("Giulia", "Neri", "D004"),
            ("Marco", "Blu", "D005"),
            ("Simone", "Raponi", "D006"),
            ("Luca", "Viola", "D007"),
            ("Edoardo", "Carletti", "D008"),
            ("Franco", "Verdi", "D009"),
            ("Walter", "Pagano", "D010")
        ]
    
    def init_ui(self):
        # Prima parte
        first_part = QFrame()
        first_layout = QVBoxLayout(first_part)
        first_layout.setContentsMargins(0, 0, 0, 0)
        first_layout.setSpacing(10)

        # Agente + username + benvenuto
        top_section = QFrame()
        top_section.setFixedHeight(50)
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(10, 5, 10, 5)
        top_layout.setSpacing(7)

        agent_icon = QLabel()
        agent_icon.setPixmap(QPixmap(":/Images/Images/agente.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))

        agent_label = QLabel(self.agente_nome)
        agent_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        agent_label.setStyleSheet("color: black;")

        welcome_label = QLabel("Benvenuto Agente!")
        welcome_label.setFont(QFont("Arial", 20))
        welcome_label.setStyleSheet("color: #555;")

        top_layout.addWidget(agent_icon)
        top_layout.addWidget(agent_label)
        top_layout.addStretch()
        top_layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        top_layout.addStretch() 

        # Sezione sotto: search bar + lista detenuti
        bottom_section = QFrame()
        bottom_layout = QVBoxLayout(bottom_section)
        bottom_layout.setContentsMargins(20, 10, 20, 10)
        bottom_layout.setSpacing(10)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Inserisci il nome del detenuto...")
        self.search_bar.setFixedHeight(30)
        self.search_bar.textChanged.connect(self.filter_list)

        search_icon = QAction(QIcon(":/Images/Images/sb.png"), "sb", self.search_bar)
        self.search_bar.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)

        # Scroll area con lista detenuti
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(12)

        self.populate_list(self.detainees)

        self.scroll_area.setWidget(self.scroll_content)

        bottom_layout.addWidget(self.search_bar)
        bottom_layout.addWidget(self.scroll_area)

        # Aggiungo sopra e sotto alla prima parte
        first_layout.addWidget(top_section, stretch=1)    
        first_layout.addWidget(bottom_section, stretch=4)

        # Seconda parte
        second_part = QFrame()
        second_part.setFixedWidth(200)
        right_layout = QVBoxLayout(second_part)

        logout_button = QPushButton(" Logout")
        logout_button.setIcon(QIcon(":/Images/Images/logout.png")) 
        logout_button.setStyleSheet("padding: 5px; font-size: 14px; background color: white;")
        logout_button.setFixedWidth(120)
        logout_button.clicked.connect(self.logout)

        right_layout.addWidget(logout_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        right_layout.addStretch()

        crest = QLabel()
        crest.setPixmap(QPixmap(":/Images/Images/logo.png").scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
        right_layout.addStretch()
        right_layout.addWidget(crest, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        # Fusione delle due parti
        main_layout = QHBoxLayout()
        main_layout.addWidget(first_part, stretch=4)
        main_layout.addWidget(second_part, stretch=1) 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

        self.setLayout(main_layout)



        # Metodo per riempire la lista con box grafici
    def populate_list(self, data):
        # Svuota layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for nome, cognome, matricola in data:
            row = QFrame()
            row.setStyleSheet("background: white; border-radius: 15px;")
            row.setFixedHeight(65)

            grid = QGridLayout(row)
            grid.setContentsMargins(20, 10, 20, 10)
            grid.setHorizontalSpacing(40)
            grid.setVerticalSpacing(0)

            # Nome con icona
            nome_layout = QHBoxLayout()
            nome_layout.setContentsMargins(0, 0, 0, 0)
            nome_layout.setSpacing(5)
            nome_icon = QLabel()
            nome_icon.setPixmap(QPixmap(":/Images/Images/user.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
            nome_label = QLabel(nome)
            nome_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            
            if nome == "Detenuto non trovato":
                nome_label.setStyleSheet("color: red;")
            else:
                nome_label.setStyleSheet("color: black;")
                
            nome_layout.addWidget(nome_icon)
            nome_layout.addWidget(nome_label)

            # Cognome
            cognome_label = QLabel(cognome)
            cognome_label.setFont(QFont("Arial", 12))
            cognome_label.setStyleSheet("color: black;")

            # Matricola con icona
            matricola_layout = QHBoxLayout()
            matricola_layout.setContentsMargins(0, 0, 0, 0)
            matricola_layout.setSpacing(5)
            matricola_icon = QLabel()
            matricola_icon.setPixmap(QPixmap(":/Images/Images/id.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
            matricola_label = QLabel(matricola)
            matricola_label.setFont(QFont("Arial", 12))
            matricola_label.setStyleSheet("color: black;")
            matricola_layout.addWidget(matricola_icon)
            matricola_layout.addWidget(matricola_label)

            # Bottone Visualizza
            view_button = QPushButton("Visualizza Detenuto")
            view_button.setFixedSize(120, 35)
            view_button.setStyleSheet("""
                QPushButton {
                    background-color: #666;
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
            """)
            view_button.clicked.connect(lambda _, n=nome, c=cognome, m=matricola: self.apri_detenuto(n, c, m))

            # Inserimento nella griglia
            grid.addLayout(nome_layout,      0, 0)
            grid.addWidget(cognome_label,    0, 1)
            grid.addLayout(matricola_layout, 0, 2)
            grid.addWidget(view_button,      0, 3, alignment=Qt.AlignmentFlag.AlignRight)

            # Box occupa tutta la larghezza disponibile
            row.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            self.scroll_layout.addWidget(row)



    # Metodo per filtro
    def filter_list(self, notFound):
        filtro = self.search_bar.text().strip().lower()
        if not filtro:
            self.populate_list(self.detainees)
            return

        filtrati = []
        for nome, cognome, matricola in self.detainees:
            if (filtro in nome.lower() or 
                filtro in cognome.lower() or 
                filtro in matricola.lower()):
                filtrati.append((nome, cognome, matricola))

        if filtrati:
            self.populate_list(filtrati)
        else:
            # Nessun risultato
            self.populate_list([("Detenuto non trovato", " ", "D000")])

    def logout(self):
        self.close()
        from view.LoginView.Login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
            
    def apri_detenuto(self, nome, cognome, matricola):
        self.detenuto_window = VisualizzaDetenutoWindow(nome, cognome, matricola)
        self.detenuto_window.show()

