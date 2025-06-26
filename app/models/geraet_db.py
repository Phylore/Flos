from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.zustand_db import Zustand
from app.models.historie_db import Historie
from app.models.geraetetest_db import GeraeteTestDurchlauf  # ganz oben ergänzen


class Geraet(db.Model):
    __tablename__ = "geraete"

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.String, unique=True, nullable=False)
    modell_id = db.Column(
        db.Integer,
        db.ForeignKey("modell.id", name="fk_geraete_modell_id"),
        nullable=False
    )
    charge_id = db.Column(
        db.Integer,
        db.ForeignKey('charge.id', name="fk_geraete_charge_id"),
        nullable=True
    )
    zustand_id = db.Column(
        db.Integer,
        db.ForeignKey("zustaende.id", name="fk_geraete_zustand_id"),
        nullable=False
    )
    benutzer_id = db.Column(
        db.Integer,
        db.ForeignKey("benutzer.id", name="fk_geraete_benutzer_id"),
        nullable=True
    )
    status = db.Column(db.String, nullable=False, server_default="Unbekannt")
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

