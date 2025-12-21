from enum.stato_verbale import StatoVerbale
from model.rapporti.rapporto_disciplinare import RapportoDisciplinare

class Verbale:
    # codiceProtocollo string, statoVerbale
    def __init__(self, codiceProtocollo: str, statoVerbale: StatoVerbale, listaRapporti: RapportoDisciplinare):
        self.codiceProtocollo = codiceProtocollo
        self.statoVerbale = statoVerbale
        self.listaRapporti = listaRapporti