from model.detenuto.dato_anagrafico import DatoAnagrafico
from model.detenuto.pena import Pena
from model.detenuto.ubicazione import Ubicazione

class Detenuto:
    def __init__(self, matricola: str, dati_anagrafici: DatoAnagrafico, pena: Pena, ubicazione: Ubicazione):
        self.matricola = matricola
        self.dati_anagrafici = dati_anagrafici
        self.pena = pena
        self.ubicazione = ubicazione