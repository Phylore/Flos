# /app/models/teil_db.py

from database import db
from sqlalchemy.orm import relationship

class Teil(db.Model):
    __tablename__ = "teile"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    modul_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
    zustand_id = db.Column(db.Integer, db.ForeignKey("zustaende.id"), nullable=False)

    modul = relationship("Modul", back_populates="teile")
    zustand = relationship("Zustand")

