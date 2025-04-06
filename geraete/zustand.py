# geraete/zustand.py
from enum import Enum

class Zustand(Enum):
    NEU = "neu"
    GEBRAUCHT = "gebraucht"
    DEFEKT = "defekt"
    GETESTET = "getestet"
    AUSSORTIERT = "ausgesondert"
    EINGELAGERT = "eingelagert"

