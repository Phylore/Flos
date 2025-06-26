from database import db

class Lieferant(db.Model):
    __tablename__ = "lieferant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    kontakt = db.Column(db.String(100))  # Optional, z.B. E-Mail/Telefon etc.
    chargen = db.relationship('Charge', back_populates='lieferant', lazy=True)

