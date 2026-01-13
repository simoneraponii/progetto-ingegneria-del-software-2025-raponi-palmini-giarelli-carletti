from datetime import datetime
from dao.main_dao import MainDAO
from model.DTO.detenuto_dto import DetenutoDTO
from model.detenuto.pena import Pena
from model.detenuto.detenuto import Detenuto
from model.detenuto.dato_anagrafico import DatoAnagrafico
from model.detenuto.ubicazione import Ubicazione

class DetenutoDAO(MainDAO):
    def __init__(self):
        super().__init__()

    # --- CONTROLLI ESISTENZA ---
    def check_esistenza_pena(self, descrizione: str, data_fine: str) -> bool:
        sql = "SELECT 1 FROM Pena WHERE descrizione = ? AND dataFinePena = ?"
        try:
            self.connect()
            try:
                data_fine_obj = datetime.strptime(data_fine, "%Y-%m-%d")
            except ValueError:
                data_fine_obj = datetime.strptime(data_fine, "%d/%m/%Y")
            self.cursor.execute(sql, (descrizione, data_fine_obj))
            row = self.cursor.fetchone()
            return row is not None
        except Exception as e:
            raise Exception(f"Errore durante il controllo di esistenza della pena: {e}")
        

    def check_esistenza_dato_anagrafico(self, codice_fiscale: str) -> bool:
        sql = "SELECT 1 FROM DatoAnagrafico WHERE codiceFiscale = ?"
        try:
            self.connect()
            self.cursor.execute(sql, (codice_fiscale,))
            row = self.cursor.fetchone()
            return row is not None
        except Exception as e:
            raise Exception(f"Errore durante il controllo del dato anagrafico: {e}")
        

    def get_id_ubicazione(self, sezione: str, camera: str) -> int:
        sql = "SELECT id FROM Ubicazione WHERE sezione = ? AND camera = ?"
        try:
            self.connect()
            self.cursor.execute(sql, (sezione, camera))
            row = self.cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise Exception(f"Errore durante il recupero dell'id_ubicazione: {e}")
        

    # --- CREAZIONE DETENUTO ---
    def create_detenuto(self, dati: dict) -> bool:
        try:
            self.connect()
            

            # DatoAnagrafico
            anagrafica = dati.get("datoAnagrafico", {})
            data_nascita_str = anagrafica.get("dataNascita") # Stringa 'YYYY-MM-DD'
            data_nascita_obj = datetime.strptime(data_nascita_str, "%Y-%m-%d")

            sql_anagrafica = """
                INSERT INTO DatoAnagrafico (codiceFiscale, nome, cognome, dataNascita, luogoNascita)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(sql_anagrafica, (
                anagrafica.get("codiceFiscale"),
                anagrafica.get("nome"),
                anagrafica.get("cognome"),
                data_nascita_obj,   # YYYY-MM-DD
                anagrafica.get("luogoNascita")
            ))
            fk_cf = anagrafica.get("codiceFiscale")

            # Pena
            pena = dati.get("pena", {})
            data_fine_str = pena.get("dataFinePena")
            data_fine_obj = datetime.strptime(data_fine_str, "%Y-%m-%d")
            sql_pena = "INSERT INTO Pena (descrizione, dataFinePena) OUTPUT INSERTED.id VALUES (?, ?)"
            self.cursor.execute(sql_pena, (
                pena.get("descrizione"),
                data_fine_obj          # YYYY-MM-DD
            ))
            id_pena = self.cursor.fetchone()[0]

            # Ubicazione
            # Ubicazione
            ubicazione = dati.pop("ubicazione", None)
            if not ubicazione:
                raise Exception("Ubicazione obbligatoria per il detenuto")
            if ubicazione:
                sezione = ubicazione.get("sezione")
                camera = ubicazione.get("camera") or ubicazione.get("cella")

                if not sezione or not camera:
                    raise Exception("Sezione e camera sono obbligatorie")

                id_ubicazione = self.get_id_ubicazione(sezione, camera)

                if id_ubicazione is None:
                    raise Exception(
                        f"Ubicazione non esistente (Sezione: {sezione}, Camera: {camera})"
                    )

                dati["id_ubicazione"] = id_ubicazione


            detenuto = dati.get("detenuto", {})
            matricola = detenuto.get("matricola")

            if not matricola:
                raise Exception("Matricola obbligatoria")

            sql = """
            INSERT INTO Detenuto (matricola, fk_codiceFiscale, id_ubicazione, id_pena)
            VALUES (?, ?, ?, ?)
            """

            self.cursor.execute(sql, (
                matricola,
                fk_cf,
                id_ubicazione,
                id_pena
            ))

            self.conn.commit()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Errore: {e}")
            return False
        

    # --- AGGIORNAMENTO DETENUTO ---
    def update_detenuto(self, matricola: str, nuovi_dati: dict) -> bool:
        try:
            self.connect()

            # ---- UBICAZIONE ----
            ubicazione = nuovi_dati.get("ubicazione")
            if ubicazione:
                self.cursor.execute(
                """
                SELECT fk_codiceFiscale, id_pena, id_ubicazione
                FROM Detenuto
                WHERE matricola = ?
                """,
                (matricola,)
            )
            row = self.cursor.fetchone()
            if not row:
                return False

            fk_cf, id_pena, id_ubicazione = row

            # ---- DATI ANAGRAFICI ----
            dati_anagrafici = nuovi_dati.get("dati_anagrafici")
            if dati_anagrafici:
                dati_anagrafici.pop("codiceFiscale", None)

                update = {}
                for k in ("nome", "cognome", "luogoNascita", "dataNascita"):
                    if k in dati_anagrafici:
                        update[k] = dati_anagrafici[k]

                if "dataNascita" in update:
                    update["dataNascita"] = datetime.strptime(
                        update["dataNascita"], "%Y-%m-%d"
                    )

                campi = ", ".join([f"{k} = ?" for k in update])
                valori = list(update.values()) + [fk_cf]

                self.cursor.execute(
                    f"UPDATE DatoAnagrafico SET {campi} WHERE codiceFiscale = ?",
                    valori
                )

            # ---- PENA ----
            pena = nuovi_dati.get("pena")
            if pena:
                update = {}
                if isinstance(pena.get("descrizione"), str):
                    update["descrizione"] = pena["descrizione"]

                if isinstance(pena.get("dataFinePena"), str):
                    update["dataFinePena"] = datetime.strptime(
                        pena["dataFinePena"], "%Y-%m-%d"
                    )

                campi = ", ".join([f"{k} = ?" for k in update])
                valori = list(update.values()) + [id_pena]

                self.cursor.execute(
                    f"UPDATE Pena SET {campi} WHERE id = ?",
                    valori
                )

             # ---- UBICAZIONE ----
            ubicazione = nuovi_dati.get("ubicazione")
            if ubicazione:
                sezione = ubicazione.get("sezione")
                camera = ubicazione.get("camera") or ubicazione.get("cella")

                if not sezione or not camera:
                    raise Exception("Sezione e camera sono obbligatorie")

                # Verifica esistenza ubicazione
                id_nuova_ubicazione = self.get_id_ubicazione(sezione, camera)

                if id_nuova_ubicazione is None:
                    raise Exception(
                        f"Ubicazione non esistente (Sezione: {sezione}, Camera: {camera})"
                    )

                # Aggiorna FK nel Detenuto
                self.cursor.execute(
                    """
                    UPDATE Detenuto
                    SET id_ubicazione = ?
                    WHERE matricola = ?
                    """,
                    (id_nuova_ubicazione, matricola)
                )  

            self.conn.commit()
            return True

        except Exception as e:
            self.conn.rollback()
            raise

        

    # --- RECUPERO DETENUTO ---
    def get_by_matricola(self, matricola: str) -> Detenuto:
        sql = """
            SELECT 
                d.matricola,                  -- 0
                da.codiceFiscale,             -- 1
                da.nome,                      -- 2
                da.cognome,                   -- 3
                da.dataNascita,               -- 4
                da.luogoNascita,              -- 5

                p.id        AS id_pena,        -- 6
                p.descrizione,                -- 7
                p.dataFinePena,               -- 8

                u.id        AS id_ubicazione,  -- 9
                u.sezione,                    -- 10
                u.camera                      -- 11
            FROM Detenuto d
            JOIN DatoAnagrafico da ON d.fk_codiceFiscale = da.codiceFiscale
            JOIN Pena p ON d.id_pena = p.id
            JOIN Ubicazione u ON d.id_ubicazione = u.id
            WHERE d.matricola = ?
        """
        try:
            self.connect()
            self.cursor.execute(sql, (matricola,))
            row = self.cursor.fetchone()
            if not row:
                return None

            columns = [col[0] for col in self.cursor.description]
            data = dict(zip(columns, row))

            dato_anagrafico = DatoAnagrafico(
                codice_fiscale=data["codiceFiscale"],
                nome=data["nome"],
                cognome=data["cognome"],
                data_nascita=data["dataNascita"],
                luogo_nascita=data["luogoNascita"]
            )

            pena = Pena(
                id=data["id_pena"],
                descrizione=data["descrizione"],
                dataFinePena=data["dataFinePena"]
            )

            ubicazione = Ubicazione(
                id=data["id_ubicazione"],
                sezione=data["sezione"],
                camera=data["camera"],
                numMaxDetenuti=0
            )

            return Detenuto(
                matricola=data["matricola"],
                dati_anagrafici=dato_anagrafico,
                pena=pena,
                ubicazione=ubicazione
            )
        except Exception as e:
            raise Exception(f"Errore nel recupero dettagliato del detenuto: {e}")
        

    # --- DTO PER LISTE ---
    def get_all_detenuti_dto(self) -> list[DetenutoDTO]:
        sql = """
            SELECT d.matricola, da.nome, da.cognome
            FROM Detenuto d
            JOIN DatoAnagrafico da ON d.fk_codiceFiscale = da.codiceFiscale
        """
        try:
            self.connect()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return [DetenutoDTO(matricola=r[0], nome=r[1], cognome=r[2]) for r in rows]
        except Exception as e:
            raise Exception(f"Errore durante il recupero dei detenuti: {e}")
        
