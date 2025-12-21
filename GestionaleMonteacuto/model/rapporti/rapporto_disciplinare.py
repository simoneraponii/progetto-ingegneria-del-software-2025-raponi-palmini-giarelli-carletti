import datetime
from model.user.user import User

class RapportoDisciplinare:
    def __init__(self, descrzione: str, data:datetime, utente: User):
        self.descrzione = descrzione
        self.data = data
        self.utente = utente