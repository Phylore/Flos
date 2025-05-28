# /app/models/kategorie_db.py

from database import db

class Kategorie(db.Model):
    __tablename__ = "kategorie"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    modelle = db.relationship("Modell", back_populates="kategorie", lazy=True)
    unterkategorien = db.relationship("Unterkategorie", backref="kategorie", lazy=True)

    def __repr__(self):
        return f"<Kategorie {self.name}>"


class Unterkategorie(db.Model):
    __tablename__ = "unterkategorie"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    kategorie_id = db.Column(db.Integer, db.ForeignKey("kategorie.id"), nullable=False)

    def __repr__(self):
        return f"<Unterkategorie {self.name} ({self.kategorie_id})>"

