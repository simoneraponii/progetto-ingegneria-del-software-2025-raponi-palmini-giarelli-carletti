from main_dao import MainDAO
from model.DTO.detenuto_dto import DetenutoDTO
from model.detenuto.pena import Pena
from model.detenuto.detenuto import Detenuto
from model.detenuto.dato_anagrafico import DatoAnagrafico
from model.detenuto.ubicazione import Ubicazione

class DetenutoDAO(MainDAO):
    def __init__(self):
        super().__init__()

    
    # --- METODI DI CONTROLLO ESISTENZA PENE E DATI ANAGRAFICI ---
    def check_esistenza_pena(self, pena:Pena):
        sql = "SELECT 1 FROM Pena WHERE descrizione = ? and dataFinePena = ?"
        try:
            self.connect()
            self.cursor.execute(sql, (pena.descrizione, pena.dataFinePena))
            row = self.cursor.fetchone()
            return row is not None
        except Exception as e:
            raise Exception(f"Errore durante il controllo di esistenza della pena: {e}")

    def check_esistenza_dato_anagrafico(self, dato: DatoAnagrafico):
        sql = "SELECT 1 FROM DatoAnagrafico WHERE codiceFiscale = ?"
        try:
            self.connect()
            self.cursor.execute(sql, (dato.codiceFiscale,))
            row = self.cursor.fetchone()
            return row is not None
        except Exception as e:
            raise Exception(f"Errore durante il controllo di esistenza del dato anagrafico: {e}")


    # --- METODI CU DETENUTO ---
    def create_detenuto(self, detenuto: Detenuto) -> bool:
        try:
            self.connect()
            # Insert DatoAnagrafico
            sql_anagrafica = "INSERT INTO DatoAnagrafico (codiceFiscale, nome, cognome, dataNascita, luogoNascita) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(sql_anagrafica, (detenuto.dati_anagrafici.codiceFiscale, detenuto.dati_anagrafici.nome, detenuto.dati_anagrafici.cognome, detenuto.dati_anagrafici.dataNascita, detenuto.dati_anagrafici.luogoNascita))
            fk_codiceFiscale = self.cursor.lastrowid

            # Insert Pena
            sql_pena = "INSERT INTO Pena (descrizione, dataFinePena) VALUES (?, ?)"
            self.cursor.execute(sql_pena, (detenuto.pena.descrizione, detenuto.pena.dataFinePena))
            id_pena = self.cursor.lastrowid

            #insert detenuto
            sql = "INSERT INTO Detenuto (matricola, id_ubicazione, id_pena, fk_codiceFiscale) VALUES (?, ?, ?, ?)"
            self.cursor.execute(sql, (detenuto.matricola, detenuto.ubicazione.id_ubicazione, id_pena, fk_codiceFiscale))
            self.conn.commit()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Errore durante la creazione del detenuto: {e}")

    def update_detenuto(self, matricola:str, nuovi_dati:dict) -> bool:
        try:
            self.connect()
            self.cursor.execute("SELECT id_anagrafica, id_pena FROM Detenuto WHERE matricola = ?", (matricola,))
            ids = self.cursor.fetchone()
            if not ids:
                return False
            id_anagrafica, id_pena = ids

            # Update DatoAnagrafico
            if 'dati_anagrafici' in nuovi_dati:
                dati_anagrafici = nuovi_dati.pop('dati_anagrafici')
                campi_anagrafica = ", ".join([f"{k} = ?" for k in dati_anagrafici.keys()])
                valori_anagrafica = list(dati_anagrafici.values())
                valori_anagrafica.append(id_anagrafica)
                sql_anagrafica = f"UPDATE DatoAnagrafico SET {campi_anagrafica} WHERE id_anagrafica = ?"
                self.cursor.execute(sql_anagrafica, valori_anagrafica)
            # Update Pena
            if 'pena' in nuovi_dati:
                pena = nuovi_dati.pop('pena')
                campi_pena = ", ".join([f"{k} = ?" for k in pena.keys()])
                valori_pena = list(pena.values())
                valori_pena.append(id_pena)
                sql_pena = f"UPDATE Pena SET {campi_pena} WHERE id_pena = ?"
                self.cursor.execute(sql_pena, valori_pena)
            # Update Detenuto
            if nuovi_dati:
                campi_detenuto = ", ".join([f"{k} = ?" for k in nuovi_dati.keys()])
                valori_detenuto = list(nuovi_dati.values())
                valori_detenuto.append(matricola)
                sql_detenuto = f"UPDATE Detenuto SET {campi_detenuto} WHERE matricola = ?"
                self.cursor.execute(sql_detenuto, valori_detenuto)
            self.conn.commit()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Errore durante l'aggiornamento del detenuto: {e}")

    # --- METODI DI RECUPERO DETENUTO ---
    def get_by_matricola(self, matricola: str) -> Detenuto:
        # Specifichiamo i campi uno per uno per evitare collisioni di nomi
        sql = """ 
            SELECT 
                d.matricola,
                da.id_anagrafica, da.codiceFiscale, da.nome, da.cognome, da.dataNascita, da.luogoNascita,
                p.id_pena, p.descrizione, p.dataFinePena,
                u.id_ubicazione, u.settore, u.cella
            FROM Detenuto d 
            JOIN DatoAnagrafico da ON d.fk_codiceFiscale = da.id_anagrafica 
            JOIN Pena p ON d.id_pena = p.id_pena 
            JOIN Ubicazione u ON d.id_ubicazione = u.id_ubicazione 
            WHERE d.matricola = ? 
        """
        try:
            self.connect()
            self.cursor.execute(sql, (matricola,))
            row = self.cursor.fetchone()
            
            if row:
                columns = [column[0] for column in self.cursor.description]
                data = dict(zip(columns, row))

                # Costruiamo i sotto-oggetti usando le chiavi specifiche del dizionario
                dato_anagrafico = DatoAnagrafico(
                    codiceFiscale=data['codiceFiscale'],
                    nome=data['nome'],
                    cognome=data['cognome'],
                    dataNascita=data['dataNascita'],
                    luogoNascita=data['luogoNascita']
                )
                
                pena = Pena(
                    descrizione=data['descrizione'],
                    dataFinePena=data['dataFinePena']
                )
                
                ubicazione = Ubicazione(
                    id_ubicazione=data['id_ubicazione'],
                    settore=data['settore'],
                    cella=data['cella']
                )
                
                # Creiamo l'oggetto radice
                return Detenuto(
                    matricola=data['matricola'],
                    dati_anagrafici=dato_anagrafico,
                    pena=pena,
                    ubicazione=ubicazione
                )
            return None
        except Exception as e:
            raise Exception(f"Errore nel recupero dettagliato del detenuto: {e}")

    def get_all_detenuti_dto(self) -> list[DetenutoDTO]:
        sql = "SELECT matricola, nome, cognome FROM Detenuto d JOIN DatoAnagrafico da ON d.fk_codiceFiscale = da.id_anagrafica"
        try:
            self.connect()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            detenuti = []
            for row in rows:
                detenuti.append(DetenutoDTO(matricola=row[0], nome=row[1], cognome=row[2]))
            return detenuti
        except Exception as e:
            raise Exception(f"Errore durante il recupero dei detenuti: {e}")
