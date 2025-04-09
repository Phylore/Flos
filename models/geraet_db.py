# /app/models/geraet_db.py

from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.zustand_db import Zustand
from models.historie_db import Historie

class Geraet(db.Model):
    __tablename__ = "geraete"

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.String, unique=True, nullable=False)
    modell_id = db.Column(db.Integer, db.ForeignKey("modell.id"), nullable=False)
    zustand_id = db.Column(db.Integer, db.ForeignKey("zustaende.id"), nullable=False)
    benutzer_id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), nullable=False)

    modell = db.relationship("Modell", back_populates="geraete")
    zustand = db.relationship("Zustand")
    benutzer = db.relationship("Benutzer", backref="geraete")
    historie = db.relationship("Historie", backref="geraet", lazy=True)


