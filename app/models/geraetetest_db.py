# Datei: models/geraete_test_db.py

from database import db

class GeraeteTestSchritt(db.Model):
    __tablename__ = "geraete_test_schritt"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    beschreibung = db.Column(db.Text, nullable=True)
    modul_name = db.Column(db.String, nullable=True)  # NEU

class GeraeteTestDurchlauf(db.Model):
    __tablename__ = "geraete_test_durchlauf"
    id = db.Column(db.Integer, primary_key=True)
    geraet_id = db.Column(db.Integer, db.ForeignKey("geraete.id"), nullable=False)
    benutzer_id = db.Column(db.Integer, db.ForeignKey("benutzer.id"), nullable=False)
    zeitpunkt = db.Column(db.DateTime, server_default=db.func.now())

    geraet = db.relationship("Geraet", back_populates="testdurchlaeufe", lazy="joined")
    ergebnisse = db.relationship("GeraeteTestErgebnis", back_populates="durchlauf", cascade="all, delete-orphan")

class GeraeteTestErgebnis(db.Model):
    __tablename__ = "geraete_test_ergebnis"
    id = db.Column(db.Integer, primary_key=True)
    durchlauf_id = db.Column(db.Integer, db.ForeignKey("geraete_test_durchlauf.id"), nullable=False)
    schritt_id = db.Column(db.Integer, db.ForeignKey("geraete_test_schritt.id"), nullable=False)
    bestanden = db.Column(db.Boolean, nullable=True)
    kommentar = db.Column(db.Text)

    durchlauf = db.relationship("GeraeteTestDurchlauf", back_populates="ergebnisse")
    schritt = db.relationship("GeraeteTestSchritt")

