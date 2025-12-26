from dao.account_dao import AccountDAO
from model.user.login_result import LoginResult
from model.enum.login_response import LoginResponse
import bcrypt

class LoginController:
    def __init__(self):
        self.accountDao = AccountDAO()

    def login(self, username: str, password: str) -> LoginResult:
        #chiamata al dao che ritorna l'utente
        try:
            loggingUser = self.accountDao.get_by_username(username)
            #se l'utente non esiste ritorno loginResult con utente None e risposta USER_NOT_FOUND
            if loggingUser is None:
                return LoginResult(utente=None, risposta=LoginResponse.USER_NOT_FOUND)
            #se l'utente esiste
            #controllo se è bloccato (tentativi rimasti 0)
            if loggingUser.tentativi <= 0:
                return LoginResult(utente =None, risposta=LoginResponse.ACCOUNT_BLOCKED)

            #controllo passwordccon la password hashata salvata nel db
            password_hashed = password.encode('utf-8')
            password_stored_hashed = loggingUser.password.encode('utf-8')
            if bcrypt.checkpw(password_hashed, password_stored_hashed):
                #se la password è corretta creo un oggetto loginResult impostando la session e con la risposta OK
                #rimetto i tentativi rimasti a 3 nel db
                self.accountDao.update(loggingUser.username, {"tentativi": 3})
                #creo oggetto globale sessione e lo imposto con l'utente loggato
                return LoginResult(utente=loggingUser, risposta=LoginResponse.OK)
            else:
                self.accountDao.update(loggingUser.username, {"tentativi": loggingUser.tentativi - 1})
                if loggingUser.tentativi - 1 <= 0:
                    return LoginResult(utente=None, risposta=LoginResponse.JUST_BLOCKED)
                else:
                    return LoginResult(utente=None, risposta=LoginResponse.WRONG_PASSWORD)
            #se la password è errata decremento i tentativi rimasti dell'utente nel db
            #cosi facendo se l'utente volesse cambiare account e fare login con un altro account ha comunque 3 tentativi
            #se i tentativi rimasti diventano 0 ritorno loginResult con utente None e risposta USER_LOCKED
        except Exception as e:
            raise Exception(f"Errore nel recupero dell'utente '{username}': {e}")
        
