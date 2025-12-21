#id sezione, camera, numMaxDetenuti, detenutiPresenti
from typing import List
from detenuto import Detenuto

class Ubicazione:
    def __init__(self, id: int, sezione: str, camera: str, numMaxDetenuti: int, detenutiPresenti: list[Detenuto]):
        self.id = id
        self.sezione = sezione
        self.camera = camera
        self.numMaxDetenuti = numMaxDetenuti
        self.detenutiPresenti = detenutiPresenti