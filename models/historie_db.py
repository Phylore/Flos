# models/historie_db.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Historie(Base):
    __tablename__ = "historie"

    id = Column(Integer, primary_key=True)
    geraet_id = Column(Integer, ForeignKey("geraete.id"), nullable=False)
    benutzer_id = Column(Integer, ForeignKey("benutzer.id"), nullable=False)
    aktion = Column(String, nullable=False)
    zeitpunkt = Column(DateTime, default=datetime.utcnow)

    benutzer = relationship("Benutzer")  # für Template-Zugriff: eintrag.benutzer.name

