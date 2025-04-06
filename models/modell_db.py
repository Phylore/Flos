# modelle/modell_db.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Modell(Base):
    __tablename__ = "modelle"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    kategorie = Column(String)

    # später: Beziehung zu Geräten
    # geraete = relationship("Geraet", back_populates="modell")

