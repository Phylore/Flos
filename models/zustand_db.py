# models/zustand_db.py
from database import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint

class Zustand(Base):
    __tablename__ = "zustaende"

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    kategorie = Column(String, nullable=False)  # z. B. "Anwesenheit", "Sauberkeit", "Funktioniert"

    __table_args__ = (
        UniqueConstraint("value", "kategorie", name="uix_value_kategorie"),
    )

    def __repr__(self):
        return f"<Zustand {self.kategorie}: {self.value}>"
