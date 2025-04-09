# /app/models/modell_db.py
from models.modul_db import Modul
from sqlalchemy.orm import relationship
from database import db

class Modell(db.Model):
    __tablename__ = "modell"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    kategorie_id = db.Column(db.Integer, db.ForeignKey("kategorie.id"), nullable=False)

    kategorie = db.relationship("Kategorie", back_populates="modelle")
    geraete = db.relationship("Geraet", back_populates="modell")
    module = db.relationship(Modul, back_populates="modell", cascade="all, delete-orphan")




    def __repr__(self):
        return f"<Modell {self.name}>"

