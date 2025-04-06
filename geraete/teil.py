# geraete/teil.py
from .zustand import Zustand

class Teil:
    def __init__(self, name: str, zustand: Zustand = Zustand.NEU):
        self.name = name
        self.zustand = zustand

    def setze_zustand(self, neuer_zustand: Zustand):
        self.zustand = neuer_zustand

    def __repr__(self):
        return f"<Teil: {self.name}, Zustand: {self.zustand.value}>"

