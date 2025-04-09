from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from .zustand_db import Zustand

db = SQLAlchemy()

class Teil(db.Model):
    __tablename__ = "teile"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    modul_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
    zustand_id = db.Column(db.Integer, db.ForeignKey("zustaende.id"), nullable=False)

    modul = relationship("Modul", back_populates="teile")
    zustand = relationship("Zustand")

# === Teilekonstanten, gruppiert nach Modultyp ===

# Modul: Station
STROMKABEL = "Stromkabel"
WASSERTANK = "Wassertank"
ABWASSERTANK = "Abwassertank"
STAUBBEUTEL = "Staubbeutel"
BASIS = "Basis"
RAMPE = "Rampe"
WASCHMODUL = "Waschmodul"
HEISSWASSERTANK = "HEISSWASSERTANK"


# Modul: Roboter
HAUPTBÜRSTE = "Hauptbürste"
NEBENBÜRSTE = "Nebenbürste"
WISCHPADHALTER = "Wischpadhalter"
WISCHPADS = "Wischpads"
STAUBBEHÄLTER = "Staubbehälter"
STAUBFILTER = "Staubfilter"

# Optional: Weitere Kategorien wie Ersatzteile oder Anleitung können separat behandelt werden

