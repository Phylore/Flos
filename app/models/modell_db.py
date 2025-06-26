# /app/models/modell_db.py
from app.models.modul_db import Modul
from app.models.hersteller_db import Hersteller  # NEU: Hersteller importieren
from sqlalchemy.orm import relationship
from database import db

class Modell(db.Model):
    __tablename__ = "modell"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    kategorie_id = db.Column(db.Integer, db.ForeignKey("kategorie.id"), nullable=False)

    unterkategorie_id = db.Column(db.Integer, db.ForeignKey("unterkategorie.id"), nullable=True)
    unterkategorie = db.relationship("Unterkategorie", backref="modelle")

    
    # NEU: Hersteller-Zuweisung
    hersteller_id = db.Column(db.Integer, db.ForeignKey("hersteller.id"), nullable=False)
    hersteller = db.relationship("Hersteller", backref="modelle")

    kategorie = db.relationship("Kategorie", back_populates="modelle")
    geraete = db.relationship("Geraet", back_populates="modell")
    module = db.relationship(Modul, back_populates="modell", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Modell {self.name} von {self.hersteller.name if self.hersteller else 'Unbekannt'}>"

