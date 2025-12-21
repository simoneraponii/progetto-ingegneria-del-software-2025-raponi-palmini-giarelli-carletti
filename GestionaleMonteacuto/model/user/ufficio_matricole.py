from model.user.user import User
from model.enum.ruolo import Ruolo

class UfficioMatricole(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ruolo = Ruolo.UFFICIO_MATRICOLE
