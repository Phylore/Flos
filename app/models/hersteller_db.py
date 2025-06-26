# models/hersteller_db.py

from database import db

class Hersteller(db.Model):
    __tablename__ = "hersteller"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Hersteller {self.name}>"

