from model.user.user import User

class Session:
    def __init__(self, current_user : User = None):
        self.current_user = current_user

    def login(self, user : User):
        self.current_user = user

    def logout(self):
        self.current_user = None