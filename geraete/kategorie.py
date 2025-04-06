# geraete/kategorie.py
from typing import List
from .modul import Modul

class Kategorie:
    def __init__(self, name: str):
        self.name = name
        self.module: List[Modul] = []

    def add_modul(self, modul: Modul):
        self.module.append(modul)

    def get_modulnamen(self):
        return [modul.name for modul in self.module]

    def __repr__(self):
        return f"<Kategorie: {self.name}, Module: {len(self.module)}>"

