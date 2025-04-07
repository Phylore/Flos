# models/zustand_db.py
from database import Base
from sqlalchemy import Column, Integer, String

class Zustand(Base):
    __tablename__ = "zustaende"

    id = Column(Integer, primary_key=True)
    value = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Zustand {self.value}>"

