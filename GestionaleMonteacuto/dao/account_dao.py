from model.DTO.user_dto import UserDTO
from model.user.user import User
from dao.main_dao import MainDAO
from model.enum.ruolo import Ruolo

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
            self.cursor.execute(sql_query, (utente.username, utente.password, utente.nome, utente.cognome,3,utente.ruolo.value))
            self.conn.commit()
            return True
        except Exception as e:
            raise Exception(f"Errore durante la creazione dell'utente: {e}")

    def update(self,username:str, nuovi_dati:dict) -> bool:
        try:
            self.connect()
            campi = ", ".join([f"{k} = ?" for k in nuovi_dati.keys()])
            valori = list(nuovi_dati.values())
            valori.append(username)
            sql = f"UPDATE Utente SET {campi} WHERE username = ?"
            self.cursor.execute(sql, valori)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Errore durante l'aggiornamento dell'utente: {e}")

    def get_utenti_dto(self) -> list[UserDTO]:
        sql_query = "SELECT username, nome, cognome, ruolo, tentativi FROM Utente"
        try:
            self.connect()
            self.cursor.execute(sql_query)
            rows = self.cursor.fetchall()
            utenti_dto = []
            columns = [column[0] for column in self.cursor.description]

            for row in rows:
                user_data = dict(zip(columns, row))

                # Converte il ruolo da stringa a enum
                if 'ruolo' in user_data and isinstance(user_data['ruolo'], str):
                    user_data['ruolo'] = Ruolo(user_data['ruolo'])

                utenti_dto.append(UserDTO(**user_data))

            return utenti_dto
        except Exception as e:
            raise Exception(f"Errore durante il recupero degli utenti DTO: {e}")
