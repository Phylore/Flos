# geraete/modul.py
from typing import List
from .teil import Teil

class Modul:
    def __init__(self, name: str):
        self.name = name
        self.teile: List[Teil] = []

    def add_teil(self, teil: Teil):
        self.teile.append(teil)

    def get_zustandsübersicht(self):
        return {teil.name: teil.zustand.value for teil in self.teile}

    def __repr__(self):
        return f"<Modul: {self.name}, Teile: {len(self.teile)}>"

