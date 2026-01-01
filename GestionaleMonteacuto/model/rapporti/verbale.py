from model.enum.stato_verbale import StatoVerbale
 

class Verbale:
    def __init__(self, codiceProtocollo: str, titolo: str, statoVerbale: str, fk_matricola: str):
        self.codice_protocollo = codiceProtocollo
        self.fk_matricola = fk_matricola  
        self.titolo = titolo
        self.stato_verbale = statoVerbale
        self.lista_rapporti = []