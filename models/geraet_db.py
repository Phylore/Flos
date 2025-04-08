from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.modell_db import Modell
from models.zustand_db import Zustand
from models.historie_db import Historie


class Geraet(Base):
    __tablename__ = "geraete"

    id = Column(Integer, primary_key=True)
    seriennummer = Column(String, unique=True, nullable=False)
    modell_id = Column(Integer, ForeignKey("modelle.id"), nullable=False)
    zustand_id = Column(Integer, ForeignKey("zustaende.id"), nullable=False)

    # Beziehungen
    modell = relationship("Modell")
    zustand = relationship("Zustand")

    # Neu: Historie-Beziehung
    historie = relationship("Historie", backref="geraet", lazy=True)

    def __repr__(self):
        return f"<Geraet {self.seriennummer}>"

