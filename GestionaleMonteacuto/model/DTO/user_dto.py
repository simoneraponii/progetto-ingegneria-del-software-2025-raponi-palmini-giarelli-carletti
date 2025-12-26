from model.enum.ruolo import Ruolo

class UserDTO:
    def __init__(self, username: str, nome: str, cognome: str, ruolo: Ruolo, tentativi: int):
        self.username = username
        self.nome = nome
        self.cognome = cognome
        self.ruolo = ruolo
        self.tentativi = tentativi