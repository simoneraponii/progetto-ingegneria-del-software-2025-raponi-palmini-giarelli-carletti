from dao.main_dao import MainDAO
from model.rapporti.verbale import Verbale
from model.enum.stato_verbale import StatoVerbale


class RapportoDAO(MainDAO):
    def __init__(self):
        super().__init__()

    def get_protocolli_by_anno(self, anno:str) -> list[str]:
        query = "SELECT codiceProtocollo FROM Verbale WHERE codiceProtocollo LIKE ?"
        try:
            self.connect()
            self.cursor.execute(query, (f"%/{anno}",))
            result = self.cursor.fetchall()
            return [r[0] for r in result]
        except Exception as e:
            raise Exception(f"Errore durante il recupero dei codici protocollo: {e}")
            return[]
        finally:
            self.disconnect()

    def insert_verbale(self, codiceProtocollo:str,titolo:str, fk_matricola:str) -> bool:
        query = """
            INSERT INTO Verbale
            (codiceProtocollo, stato, fk_matricola, titolo)
            VALUES (?,?,?,?)
        """
        try:
            self.connect()
            self.cursor.execute(query,(codiceProtocollo, StatoVerbale.CREATED.name, fk_matricola, titolo))
            self.conn.commit()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Errore nell'inserimento: {e}")
        finally:
            self.disconnect()

    def get_verbali_by_matricola(self, matricola: str) -> list[Verbale]:
        # Query: Selezioniamo SOLO quello che serve alla tua classe
        query = """
            SELECT codiceProtocollo, titolo, stato, fk_matricola
            FROM Verbale 
            WHERE fk_matricola = ?
            ORDER BY codiceProtocollo DESC
        """
        try:
            self.connect()
            self.cursor.execute(query, (matricola,))
            rows = self.cursor.fetchall()
            
            lista_verbali = []
            for row in rows:
                v = Verbale(
                    codiceProtocollo=row[0],
                    titolo=row[1],
                    statoVerbale=row[2], 
                    fk_matricola=row[3]
                )
                lista_verbali.append(v)
            
            return lista_verbali

        except Exception as e:
            print(f"Errore DAO get_verbali: {e}")
            return []
        finally:
            self.disconnect()