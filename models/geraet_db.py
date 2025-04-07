# models/geraet_db.py
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Geraet(Base):
    __tablename__ = "geraete"

    id = Column(Integer, primary_key=True, index=True)
    seriennummer = Column(String, unique=True, nullable=False)

    modell_id = Column(Integer, ForeignKey("modelle.id"))
    zustand_id = Column(Integer, ForeignKey("zustaende.id"))

    # Beziehungen
    modell = relationship("Modell", back_populates="geraete")
    zustand = relationship("Zustand")

    def zeige_historie(self):
        # Dummy bis echte Historie kommt
        return "Historieeinträge folgen hier."

