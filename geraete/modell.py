# geraete/modell.py
from .kategorie import Kategorie

class Modell(Kategorie):
    def __init__(self, modellname: str, kategorie_name: str):
        super().__init__(kategorie_name)
        self.modellname = modellname

    def __repr__(self):
        return f"<Modell: {self.modellname}, Kategorie: {self.name}, Module: {len(self.module)}>"

