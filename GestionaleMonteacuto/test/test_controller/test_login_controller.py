import unittest
from unittest.mock import MagicMock, patch
import bcrypt

from controller.login_controller import LoginController
from model.enum.login_response import LoginResponse

class UserStub:
    def __init__(self, username:str, password:str, tentativi:int):
        self.username = username
        self.password = password
        self.tentativi = tentativi

class TestLoginController(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('controller.login_controller.AccountDAO')
        self.MockAccountDAO = self.patcher.start()
        
        self.controller = LoginController()
        self.mock_dao_instance = self.controller.accountDao
        password_in_chiaro = "passwordSegreta"
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password_in_chiaro.encode('utf-8'), salt).decode('utf-8')
        
        self.valid_username = "testuser"
        self.valid_password = "passwordSegreta"

    def tearDown(self):
        self.patcher.stop()


    def test_login_success(self):
        user = UserStub(self.valid_username, self.hashed_password, 3)
        self.mock_dao_instance.get_by_username.return_value = user
        result = self.controller.login(self.valid_username, self.valid_password) 
        self.assertEqual(result.risposta, LoginResponse.OK)
        self.assertIsNotNone(result.utente)
        self.mock_dao_instance.update.assert_called_with(self.valid_username, {"tentativi": 3})

    def test_login_user_not_found(self):
        self.mock_dao_instance.get_by_username.return_value = None
        result = self.controller.login("non_esiste", "password")
        self.assertEqual(result.risposta, LoginResponse.USER_NOT_FOUND)
        self.assertIsNone(result.utente)


    def test_login_wrong_password(self):
        user = UserStub(self.valid_username, self.hashed_password, 3)
        self.mock_dao_instance.get_by_username.return_value = user
        result = self.controller.login(self.valid_username, "passwordSbagliata")
        self.assertEqual(result.risposta, LoginResponse.WRONG_PASSWORD)
        self.assertIsNone(result.utente)
        self.mock_dao_instance.update.assert_called_with(self.valid_username, {"tentativi": 2})


    def test_login_account_already_blocked(self):
        user = UserStub(self.valid_username, self.hashed_password, 0)
        self.mock_dao_instance.get_by_username.return_value = user
        result = self.controller.login(self.valid_username, self.valid_password)
        self.assertEqual(result.risposta, LoginResponse.ACCOUNT_BLOCKED)
        self.assertIsNone(result.utente)
        self.mock_dao_instance.update.assert_not_called()


    def test_login_just_blocked(self):
        user = UserStub(self.valid_username, self.hashed_password, 1)
        self.mock_dao_instance.get_by_username.return_value = user
        result = self.controller.login(self.valid_username, "passwordSbagliata")
        self.assertEqual(result.risposta, LoginResponse.JUST_BLOCKED)
        self.mock_dao_instance.update.assert_called_with(self.valid_username, {"tentativi": 0})


    def test_login_dao_exception(self):
        self.mock_dao_instance.get_by_username.side_effect = Exception("DB Error")
        with self.assertRaises(Exception) as context:
            self.controller.login(self.valid_username, "password")
        self.assertIn("Errore nel recupero dell'utente", str(context.exception))

if __name__ == '__main__':
    unittest.main()