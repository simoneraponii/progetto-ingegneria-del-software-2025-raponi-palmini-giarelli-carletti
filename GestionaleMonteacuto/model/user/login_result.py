from model.user.user import User
from model.enum.login_response import LoginResponse


class LoginResult:
    def __init__(self, utente:User, risposta: LoginResponse):
        self.utente = utente
        self.risposta = risposta