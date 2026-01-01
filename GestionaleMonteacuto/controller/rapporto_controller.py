from datetime import datetime
from dao.rapporto_dao import RapportoDAO
from model.rapporti.verbale import Verbale


class RapportoController:
    def __init__(self):
        self.rapporto_dao = RapportoDAO()


    def genera_codice_protocollo(self) -> str:
        current_year = datetime.now().strftime("%y")
        codiciProtocolloEsistenti = self.rapporto_dao.get_protocolli_by_anno(current_year)
        nuovo_numero = 1

        if codiciProtocolloEsistenti:
            numeri_usati = []
            for codice in codiciProtocolloEsistenti:
                try:
                    #xxx/yyy mi serve la parte xxx
                    parte_numerica = codice.split('/')[0]
                    numeri_usati.append(int(parte_numerica))
                except ValueError:
                    continue
            if numeri_usati:
                nuovo_numero = max(numeri_usati) + 1

        codProtocollo = f"{nuovo_numero:03d}/{current_year}"
        return codProtocollo

    def crea_verbale(self, titolo:str, matricola:str) -> bool:
        codiceProtocollo = self.genera_codice_protocollo()
        return self.rapporto_dao.insert_verbale(codiceProtocollo, titolo, matricola)

    def get_verbali_detenuto(self, matricola: str) -> list[Verbale]:
        return self.rapporto_dao.get_verbali_by_matricola(matricola)
        