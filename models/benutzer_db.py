# models/benutzer_db.py
from database import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # ✅ Wichtig für Flask-Login

class Benutzer(Base, UserMixin):  # ✅ UserMixin eingebunden
    __tablename__ = "benutzer"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    passwort_hash = Column(String, nullable=False)

    def set_passwort(self, passwort):
        self.passwort_hash = generate_password_hash(passwort)

    def check_passwort(self, passwort):
        return check_password_hash(self.passwort_hash, passwort)

    def __repr__(self):
        return f"<Benutzer {self.name}>"

