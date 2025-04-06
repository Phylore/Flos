# geraete/geraet.py

from datetime import datetime
from typing import List
from .zustand import Zustand
from .modell import Modell

class Geraet:
    def __init__(self, seriennummer: str, modell: Modell, zustand: Zustand = Zustand.NEU):
        self.seriennummer = seriennummer
        self.modell = modell
        self.zustand = zustand
        self.historie: List[str] = []
        self.log(f"Gerät erstellt mit Zustand: {zustand.value}")

    def aktualisiere_zustand(self, neuer_zustand: Zustand):
        self.log(f"Zustand geändert von {self.zustand.value} zu {neuer_zustand.value}")
        self.zustand = neuer_zustand

    def log(self, eintrag: str):
        zeitstempel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.historie.append(f"[{zeitstempel}] {eintrag}")

    def zeige_historie(self):
        return "\n".join(self.historie)

    def __repr__(self):
        return f"<Gerät: SN {self.seriennummer}, Modell: {self.modell.modellname}, Zustand: {self.zustand.value}>"

