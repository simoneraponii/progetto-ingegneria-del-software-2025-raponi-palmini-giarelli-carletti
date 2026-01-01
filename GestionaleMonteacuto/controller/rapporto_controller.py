from datetime import datetime
from dao.rapporto_dao import RapportoDAO
from model.enum.ruolo import Ruolo
from model.enum.stato_verbale import StatoVerbale
from model.rapporti.verbale import Verbale
from model.rapporti.rapporto_disciplinare import RapportoDisciplinare


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
    
    def get_lista_rapporti(self, codice_protocollo:str)-> list[RapportoDisciplinare]:
        return self.rapporto_dao.get_all_rapporti(codice_protocollo)

    def aggiungi_rapporto(self,oggetto:str,descrizione:str,username:str,codiceProtocollo:str) -> bool:
        return self.rapporto_dao.aggiungi_rapporto(oggetto,descrizione,username,codiceProtocollo)

    def modifica_rapporto(self, id_rapporto: int, oggetto: str, descrizione: str) -> bool:
        return self.rapporto_dao.update_rapporto(id_rapporto, oggetto, descrizione)

    def get_stato_attuale(self, protocollo: str) -> StatoVerbale | None:
        return self.rapporto_dao.get_stato_verbale(protocollo)

    def conferma_verbale(self, protocollo: str, ruolo_utente: Ruolo) -> bool:
        nuovo_stato = None
        if ruolo_utente == Ruolo.COMANDANTE:
            nuovo_stato = StatoVerbale.CONFIRMED_COMANDANTE
        elif ruolo_utente == Ruolo.UFFICIO_COMANDO:
            nuovo_stato = StatoVerbale.CONFIRMED_UFFICIO_COMANDO            

        return self.rapporto_dao.update_stato_verbale(protocollo, nuovo_stato)