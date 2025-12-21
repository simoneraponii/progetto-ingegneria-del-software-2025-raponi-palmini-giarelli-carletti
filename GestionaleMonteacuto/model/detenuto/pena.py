from datetime import datetime

class Pena:
    def __init__(self, id:int, descrizione: str, dataFinePena: datetime):
        self.id = id
        self.descrizione = descrizione
        self.dataFinePena = dataFinePena