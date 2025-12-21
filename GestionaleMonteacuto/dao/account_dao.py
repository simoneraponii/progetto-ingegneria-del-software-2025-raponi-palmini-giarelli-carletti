from model.user.user import User
from dao.main_dao import MainDAO

class AccountDAO(MainDAO):
    def __init__(self):
        super().__init__()

    def get_by_username(self,username:str) -> User:
        sql_query = "SELECT * from Utente WHERE username = ?"
        try:
            self.connect()
            self.cursor.execute(sql_query,(username,))
            row = self.cursor.fetchone()
            
            if row:
                colums = [column[0] for column in self.cursor.description]
                user_data = dict(zip(colums, row))

                return User(**user_data)
            else:
                return None
        except Exception as e:
            raise Exception(f"Errore durante il recupero dell'utente': {e}")

    def get_all(self) -> list[User]:
        sql_query = "SELECT * from Utente"
        try:
            self.connect()
            self.cursor.execute(sql_query)
            rows = self.cursor.fetchall()
            utenti = []
            colums = [column[0] for column in self.cursor.description]
            for row in rows:
                user_data = dict(zip(colums, row))
                utenti.append(User(**user_data))
            return utenti
        except Exception as e:
            raise Exception(f"Errore durante il recupero degli utenti: {e}")
    
    def create_utente(self, utente: User) -> bool:
        sql_query = "INSERT INTO Utente (username, password, nome, cognome, tentativi, ruolo) VALUES (?, ?, ?, ?, ?, ?)"
        try:
            self.connect()
            self.cursor.execute(sql_query, (utente.username, utente.password, utente.nome, utente.cognome,3,utente.ruolo))
            self.conn.commit()
            return True
        except Exception as e:
            raise Exception(f"Errore durante la creazione dell'utente: {e}")

    def update(self, utente:User, nuovi_dati:dict) -> bool:
        try:
            self.connect()
            campi = ", ".join([f"{k} = ?" for k in nuovi_dati.keys()])
            valori = list(nuovi_dati.values())
            valori.append(utente.username)
            sql = f"UPDATE Utente SET {campi} WHERE username = ?"
            self.cursor.execute(sql, valori)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Errore durante l'aggiornamento dell'utente: {e}")

