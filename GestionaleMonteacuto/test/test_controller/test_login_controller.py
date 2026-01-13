import unittest
from unittest.mock import MagicMock
import bcrypt

from controller.login_controller import LoginController
from model.enum.login_response import LoginResponse

# stub per simulare l'utente
class UserStub:
    def __init__(self, username:str, password:str, tentativi:int):
        self.username = username
        self.password = password
        self.tentativi = tentativi

class TestLoginController(unittest.TestCase):

    def setUp(self):
        self.controller = LoginController()
        self.controller.accountDao = MagicMock()
        self.valid_username = "testuser"
        self.valid_password = "passwordSegreta"

        # hashed
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(self.valid_password.encode('utf-8'), salt).decode('utf-8')

    def test_login_success(self):
        # l'utente stub qui ha 3 tentativi quindi entra
        user = UserStub(self.valid_username, self.hashed_password, 3)
        self.controller.accountDao.get_by_username.return_value = user
        
        result = self.controller.login(self.valid_username, self.valid_password)
        
        self.assertEqual(result.risposta, LoginResponse.OK)
        self.assertIsNotNone(result.utente)
        # verifica reset dopo login
        self.controller.accountDao.update.assert_called_with(self.valid_username, {"tentativi": 3})

    def test_login_user_not_found(self):
        # non trovo lo user
        self.controller.accountDao.get_by_username.return_value = None
        
        result = self.controller.login("non_esiste", "password")
        
        self.assertEqual(result.risposta, LoginResponse.USER_NOT_FOUND)
        self.assertIsNone(result.utente)

    def test_login_wrong_password(self):
        # psw sbagliata
        user = UserStub(self.valid_username, self.hashed_password, 3)
        self.controller.accountDao.get_by_username.return_value = user
        
        result = self.controller.login(self.valid_username, "passwordSbagliata")
        
        self.assertEqual(result.risposta, LoginResponse.WRONG_PASSWORD)
        self.assertIsNone(result.utente)
        #verifica decremento tentativi
        self.controller.accountDao.update.assert_called_with(self.valid_username, {"tentativi": 2})

    def test_login_account_already_blocked(self):
        user = UserStub(self.valid_username, self.hashed_password, 0)
        self.controller.accountDao.get_by_username.return_value = user
        
        result = self.controller.login(self.valid_username, self.valid_password)
        
        self.assertEqual(result.risposta, LoginResponse.ACCOUNT_BLOCKED)
        self.assertIsNone(result.utente)
        self.controller.accountDao.update.assert_not_called()

    def test_login_just_blocked(self):
        # ho un tentativo residuo e sbaglio la psw
        user = UserStub(self.valid_username, self.hashed_password, 1)
        self.controller.accountDao.get_by_username.return_value = user
        
        result = self.controller.login(self.valid_username, "passwordSbagliata")
        
        self.assertEqual(result.risposta, LoginResponse.JUST_BLOCKED)
        self.controller.accountDao.update.assert_called_with(self.valid_username, {"tentativi": 0})



if __name__ == '__main__':
    unittest.main()