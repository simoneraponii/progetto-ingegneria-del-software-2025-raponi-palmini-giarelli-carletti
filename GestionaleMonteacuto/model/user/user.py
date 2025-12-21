from abc import ABC

from model.enum.ruolo import Ruolo


class User(ABC):
    def __init__(self, username: str, password: str, nome: str, cognome: str, tentativi: int, ruolo: Ruolo):
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.tentativi = tentativi
        self.ruolo = ruolo
