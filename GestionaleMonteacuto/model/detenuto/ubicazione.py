#id sezione, camera, numMaxDetenuti, detenutiPresenti
from typing import List


class Ubicazione:
    def __init__(self, id: int, sezione: str, camera: str, numMaxDetenuti: int):
        self.id = id
        self.sezione = sezione
        self.camera = camera
        self.numMaxDetenuti = numMaxDetenuti
