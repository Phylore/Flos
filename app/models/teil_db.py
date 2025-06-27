from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.geraet_db import Geraet
from app.models.teilvorlage_db import TeilVorlage

class Teil(Base):
    __tablename__ = "teil"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    modul_id = Column(Integer, ForeignKey("modul.id"))
    geraet_id = Column(Integer, ForeignKey("geraete.id"))

    anwesenheit_id = Column(Integer, ForeignKey("zustaende.id"))
    sauberkeit_id = Column(Integer, ForeignKey("zustaende.id"))
    beschaedigung_id = Column(Integer, ForeignKey("zustaende.id"))
    teilvorlage_id = Column(Integer, ForeignKey('teilvorlage.id'))

    modul = relationship("Modul", back_populates="teile")
    anwesenheit = relationship("Zustand", foreign_keys=[anwesenheit_id])
    sauberkeit = relationship("Zustand", foreign_keys=[sauberkeit_id])
    beschaedigung = relationship("Zustand", foreign_keys=[beschaedigung_id])
    geraet = relationship("Geraet", back_populates="teile")
    teilvorlage = relationship("TeilVorlage", back_populates="vorlage_teile", overlaps="vorlage_teile")
