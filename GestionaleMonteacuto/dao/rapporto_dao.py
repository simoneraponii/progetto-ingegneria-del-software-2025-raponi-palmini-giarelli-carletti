from dao.main_dao import MainDAO
from model.rapporti.rapporto_disciplinare import RapportoDisciplinare
from model.rapporti.verbale import Verbale
from model.enum.stato_verbale import StatoVerbale
from datetime import datetime


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

    def get_all_rapporti(self, fk_codiceProtocollo:str) -> list[RapportoDisciplinare]:
        query = """
            SELECT id, oggetto, descrizione, data, fk_username, fk_codiceProtocollo 
            FROM RapportoDisciplinare 
            WHERE fk_codiceProtocollo = ?
            ORDER BY data DESC
        """
        try:
            self.connect()
            self.cursor.execute(query, (fk_codiceProtocollo,))
            rows = self.cursor.fetchall()
            
            lista_rapporti = []
            
            for row in rows:
                rapporto = RapportoDisciplinare(
                    id_rapporto=row[0],
                    oggetto=row[1],
                    descrizione=row[2],
                    data=str(row[3]),
                    fk_username=row[4],
                    fk_protocollo=row[5]
                )
                lista_rapporti.append(rapporto)
            
            return lista_rapporti

        except Exception as e:
            return []
            raise Exception(f"Errore nel recupero dei rapporti: {e}")            
        finally:
            self.disconnect()
    
    def aggiungi_rapporto(self, oggetto: str, descrizione: str, fk_username: str, fk_codiceProtocollo: str) -> bool:
        """
        Inserisce un rapporto. Passiamo un oggetto datetime al driver ODBC:
        il driver gestisce la conversione corretta verso il tipo datetime di SQL Server.
        """
        current_date = datetime.now()  # passiamo un oggetto datetime, non una stringa

        query = """
            INSERT INTO RapportoDisciplinare 
            (oggetto, descrizione, data, fk_username, fk_codiceProtocollo) 
            VALUES (?, ?, ?, ?, ?)
        """

        try:
            self.connect()

            # Passiamo current_date (datetime) al binding: il driver ODBC si occupa della conversione
            self.cursor.execute(query, (
                oggetto,
                descrizione,
                current_date,
                fk_username,
                fk_codiceProtocollo
            ))

            self.conn.commit()
            return True

        except Exception as e:
            print(f"Errore inserimento rapporto: {e}")
            if self.conn:
                self.conn.rollback()
            return False

        finally:
            self.disconnect()
   


    def update_rapporto(self, id_rapporto: int, oggetto: str, descrizione: str) -> bool:
        query = """
            UPDATE RapportoDisciplinare 
            SET oggetto = ?, descrizione = ? 
            WHERE id = ?
        """
        try:
            self.connect()
            self.cursor.execute(query, (oggetto, descrizione, id_rapporto))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Errore update rapporto: {e}")
            if self.conn: self.conn.rollback()
            return False
        finally:
            self.disconnect()

    def get_stato_verbale(self, protocollo: str) -> StatoVerbale | None:       
            query = "SELECT stato FROM Verbale WHERE codiceProtocollo = ?"
            try:
                self.connect()
                self.cursor.execute(query, (protocollo,))
                res = self.cursor.fetchone()
            
                if res:
                    # res[0] è la stringa (es. 'CREATED')
                    # La convertiamo in Enum: StatoVerbale['CREATED']
                    try:
                        return StatoVerbale[res[0]] 
                    except KeyError:
                        print(f"Errore DAO: Stato '{res[0]}' non riconosciuto nell'Enum.")
                        return None
                return None
            
            except Exception as e:
                print(f"Errore get_stato_verbale: {e}")
                return None
            finally:
                self.disconnect()

    def update_stato_verbale(self, protocollo: str, nuovo_stato: StatoVerbale | None) -> bool:
        query = "UPDATE Verbale SET stato = ? WHERE codiceProtocollo = ?"
        try:
            self.connect()
            self.cursor.execute(query, (nuovo_stato.value, protocollo))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Errore update_stato_verbale: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            self.disconnect()