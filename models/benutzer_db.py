# models/benutzer_db.py
from database import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import Boolean, DateTime
from datetime import datetime

class Benutzer(Base, UserMixin):
    __tablename__ = "benutzer"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    passwort_hash = Column(String, nullable=False)
    rolle = Column(String(20), nullable=False, default="user")
    email = Column(String(255), unique=True, nullable=True)       # Neu
    aktiv = Column(Boolean, nullable=False, default=True)         # Neu
    gesperrt = Column(Boolean, nullable=False, default=False)     # Neu
    created_at = Column(DateTime, default=datetime.utcnow)        # Neu


    def set_passwort(self, passwort):
        self.passwort_hash = generate_password_hash(passwort)

    def check_passwort(self, passwort):
        return check_password_hash(self.passwort_hash, passwort)

    def __repr__(self):
        return f"<Benutzer {self.name}>"

    @property
    def ist_admin(self):
        return self.rolle == "admin"

