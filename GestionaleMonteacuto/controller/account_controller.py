from dao.account_dao import AccountDAO
from model.user.user import User
import bcrypt

class AccountController:
    def __init__(self):
        self.accountDao = AccountDAO()

    def get_by_username(self, username: str) -> User:
        try:
            return self.accountDao.get_by_username(username)
        except Exception as e:
            raise Exception(f"Errore nel recupero dell'utente '{username}': {e}")

    def get_all(self) -> list[User]:
        try:
            return self.accountDao.get_all()
        except Exception as e:
            raise Exception(f"Errore nel recupero degli utenti: {e}")

    def create_utente(self, dati_utente: dict) -> bool:
        try:
            # dati_utente['password'] = bcrypt.hashpw(
            #     dati_utente['password'].encode('utf-8'),
            #     bcrypt.gensalt()
            # )
            psw_bytes = dati_utente['password'].encode('utf-8')
            hashed_bytes = bcrypt.hashpw(psw_bytes, bcrypt.gensalt())
            dati_utente['password'] = hashed_bytes.decode('utf-8')
            nuovo_utente = User(**dati_utente)
            return self.accountDao.create_utente(nuovo_utente)
        except Exception as e:
            raise Exception(f"Errore nella creazione dell'utente: {e}")

    def update_utente(self, utente:User, nuovi_dati: dict) -> bool:
        if "username" in nuovi_dati:
            del nuovi_dati["username"]
        if "password" in nuovi_dati:
            nuovi_dati["password"] = bcrypt.hashpw(
                nuovi_dati["password"].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
        try:
            return self.accountDao.update(utente, nuovi_dati)
        except Exception as e:
            raise Exception(f"Errore nell'aggiornamento dell'utente '{utente.username}': {e}")
