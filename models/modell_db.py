# models/modell_db.py
from database import Base  # Jetzt korrekt importieren
from sqlalchemy import Column, Integer, String

class Modell(Base):
    __tablename__ = "modelle"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    kategorie = Column(String)

