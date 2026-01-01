from datetime import datetime

class RapportoDisciplinare:
    def __init__(self, id_rapporto: int, oggetto: str, descrizione: str, data: str, fk_username: str, fk_protocollo: str):
        self.id = id_rapporto
        self.oggetto = oggetto
        self.descrizione = descrizione
        self.data = data 
        self.fk_username = fk_username     
        self.fk_protocollo = fk_protocollo   