# /app/models/geraet_db.py

from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.zustand_db import Zustand
from models.historie_db import Historie
from models.geraetetest_db import GeraeteTestDurchlauf  # ganz oben ergänzen


class Geraet(db.Model):
    __tablename__ = "geraete"

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.String, unique=True, nullable=False)
    modell_id = db.Column(db.Integer, db.ForeignKey("modell.id"), nullable=False)
    zustand_id = db.Column(db.Integer, db.ForeignKey("zustaende.id"), nullable=False)
    benutzer_id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), nullable=True)
    ausgepackt = db.Column(db.Boolean, default=False)
    gereinigt = db.Column(db.Boolean, default=False)
    getestet = db.Column(db.Boolean, default=False)
    bilder_einpackfertig = db.Column(db.Boolean, default=False)
    bilder_fertig = db.Column(db.Boolean, default=False)
    einpackbereit = db.Column(db.Boolean, default=False)
  

    modell = db.relationship("Modell", back_populates="geraete")
    zustand = db.relationship("Zustand")
    benutzer = db.relationship("Benutzer", backref="geraete")
    historie = db.relationship("Historie", backref="geraet", lazy=True)
    module = db.relationship("Modul", back_populates="geraet", cascade="all, delete-orphan")
    teile = db.relationship("Teil", back_populates="geraet")
    testdurchlaeufe = db.relationship("GeraeteTestDurchlauf", back_populates="geraet", cascade="all, delete-orphan")
