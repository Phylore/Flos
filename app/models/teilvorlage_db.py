from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class TeilVorlage(Base):
    __tablename__ = "teilvorlage"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    kategorien = Column(String)  # Optional: CSV oder später eigenes Table/Relation

    # Rückbeziehung auf Teil (Achtung, Teil wird später importiert!)
    vorlage_teile = relationship("Teil", back_populates="teilvorlage", overlaps="teilvorlage")

