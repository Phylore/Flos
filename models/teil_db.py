
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.geraet_db import Geraet  # ganz oben ergänzen

class Teil(Base):
    __tablename__ = "teil"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    modul_id = Column(Integer, ForeignKey("modul.id"))
    zustand_id = Column(Integer, ForeignKey("zustaende.id"))
    geraet_id = Column(Integer, ForeignKey("geraete.id"))  # 🆕
    
    modul = relationship("Modul", back_populates="teile")
    zustand = relationship("Zustand")
    geraet = relationship("Geraet", back_populates="teile")  # optional

# ========================
# Vorlagen für Modulimport
# ========================

class TeilVorlage:
    def __init__(self, name, kategorien=None):
        self.name = name
        self.kategorien = kategorien or []

# Stationsteile
STROMKABEL = TeilVorlage("Stromkabel", ["Saugroboter"])
WASSERTANK = TeilVorlage("Wassertank", ["Saugroboter"])
ABWASSERTANK = TeilVorlage("Abwassertank", ["Saugroboter"])
STAUBBEUTEL = TeilVorlage("Staubbeutel", ["Saugroboter"])
BASIS = TeilVorlage("Basis", ["Saugroboter"])
RAMPE = TeilVorlage("Rampe", ["Saugroboter"])
WASCHMODUL = TeilVorlage("Waschmodul", ["Saugroboter"])

# Robotermodulteile
HAUPTBÜRSTE = TeilVorlage("Hauptbürste", ["Saugroboter"])
SEITENBÜRSTE = TeilVorlage("Seitenbürste", ["Saugroboter"])
WISCHMODUL = TeilVorlage("Wischmodul", ["Saugroboter"])
WISCHPADHALTER = TeilVorlage("Wischpadhalter", ["Saugroboter"])
WISCHPADS = TeilVorlage("Wischpads", ["Saugroboter"])
STOFF = TeilVorlage("Wischstoff", ["Saugroboter"])
LASER = TeilVorlage("Lasereinheit", ["Saugroboter"])
RAD = TeilVorlage("Radmodul", ["Saugroboter"])
STAUBFILTER = TeilVorlage("Staubfilter", ["Saugroboter"])
STAUBBEHÄLTER = TeilVorlage("Staubbehälter", ["Saugroboter"])
NEBENBÜRSTE = TeilVorlage("Nebenbürste", ["Saugroboter"])

alle_teilvorlagen = [
    STROMKABEL, WASSERTANK, ABWASSERTANK, STAUBBEUTEL,
    BASIS, RAMPE, WASCHMODUL,
    HAUPTBÜRSTE, SEITENBÜRSTE, WISCHMODUL, WISCHPADHALTER,
    WISCHPADS, STOFF, LASER, RAD, STAUBFILTER, STAUBBEHÄLTER, NEBENBÜRSTE
]

