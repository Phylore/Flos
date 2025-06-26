from app.models.teil_db import Teil
from database import db
from sqlalchemy.orm import relationship

class Modul(db.Model):
    __tablename__ = "modul"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    modell_id = db.Column(db.Integer, db.ForeignKey("modell.id"), nullable=True)
    reihenfolge = db.Column(db.Integer, default=0)
    geraet_id = db.Column(db.Integer, db.ForeignKey("geraete.id"))

    geraet = relationship("Geraet", back_populates="module")
    modell = relationship("Modell", back_populates="module")
    teile = relationship("Teil", back_populates="modul", cascade="all, delete-orphan")



