# geraete/modelle/dreame.py

from geraete.modell import Modell
from geraete.modul import Modul
from geraete.teil import Teil
from geraete.zustand import Zustand

class DreameL10(Modell):
    def __init__(self):
        super().__init__("Dreame L10", "Saugroboter")

        station = Modul("Station")
        station.add_teil(Teil("Netzteil", Zustand.NEU))
        station.add_teil(Teil("Wassertank", Zustand.GEBRAUCHT))

        roboter = Modul("Roboter")
        roboter.add_teil(Teil("Sensor", Zustand.DEFEKT))
        roboter.add_teil(Teil("Bürste", Zustand.GEBRAUCHT))

        self.add_modul(station)
        self.add_modul(roboter)

class DreameD9(Modell):
    def __init__(self):
        super().__init__("Dreame D9", "Saugroboter")

        roboter = Modul("Roboter")
        roboter.add_teil(Teil("Bürste", Zustand.NEU))
        roboter.add_teil(Teil("Akku", Zustand.GEBRAUCHT))

        self.add_modul(roboter)

