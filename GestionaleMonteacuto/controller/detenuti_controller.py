from controller.rapporto_controller import RapportoController
from dao.detenuto_dao import DetenutoDAO
from model.DTO.detenuto_dto import DetenutoDTO
from model.detenuto import dato_anagrafico
from model.detenuto.detenuto import Detenuto
from model.detenuto.dato_anagrafico import DatoAnagrafico
from model.detenuto.pena import Pena
from model.detenuto.ubicazione import Ubicazione


class DetenutiController():
    def __init__(self):
        self.detenuto_dao = DetenutoDAO()
        
    def get_detenuto(self, matricola: str) -> Detenuto:
        try:
            detenuto = self.detenuto_dao.get_by_matricola(matricola)
            if detenuto is None:
                raise Exception("Detenuto non trovato")
            return detenuto
        except Exception as e:
            raise Exception(f"Errore nel recupero del detenuto: {e}")

    def update_detenuto(self, matricola, dati_dizionario) -> bool:
        try:
            if not matricola:
                print("Errore: Matricola mancante")
                return False
            successo = self.detenuto_dao.update_detenuto(matricola, dati_dizionario)
            return successo
        except Exception as e:
            print(f"Errore nel Controller durante l'update: {e}")
            return False

    def crea_nuovo_detenuto(self, dati_detenuto: dict) -> bool:
        #controllo se esiste già il dato anagrafico
        #controllo se esiste già la pena
        #controllo se esiste già l'ubicazione
        #controllo se esiste già la matricola
        try:
            id_ubicazione = self.detenuto_dao.get_id_ubicazione(dati_detenuto["ubicazione"]["sezione"], dati_detenuto["ubicazione"]["cella"])
            if id_ubicazione is None:
                return False
            if self.detenuto_dao.check_esistenza_dato_anagrafico(dati_detenuto["datoAnagrafico"]["codiceFiscale"]):
                return False
            if self.detenuto_dao.check_esistenza_pena(dati_detenuto["pena"]["descrizione"],dati_detenuto["pena"]["dataFinePena"]):
                return False
            else:
                return self.detenuto_dao.create_detenuto(dati_detenuto)
        except Exception as e:
            raise Exception(f"Errore nela creazione: {e}")
                

    def getDetenutiDto(self) -> list[DetenutoDTO]:
        try:
            return self.detenuto_dao.get_all_detenuti_dto()
        except Exception as e:
            raise Exception(f"Errore nel recupero dei detenuti: {e}")
