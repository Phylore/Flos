from models.teil_db import Teil
from database import db
from sqlalchemy.orm import relationship

class Modul(db.Model):
    __tablename__ = "modul"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    modell_id = db.Column(db.Integer, db.ForeignKey("modell.id"), nullable=False)
    reihenfolge = db.Column(db.Integer, default=0)

    modell = relationship("Modell", back_populates="module")
    teile = relationship("Teil", back_populates="modul", cascade="all, delete-orphan")



