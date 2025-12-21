from datetime import datetime

# codiceFiscale, nome, cognome, dataNascita, luogoNascita

class DatoAnagrafico:
    def __init__(self, codice_fiscale: str, nome: str, cognome: str, data_nascita: datetime, luogo_nascita: str):
        self.codice_fiscale = codice_fiscale
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.luogo_nascita = luogo_nascita
    