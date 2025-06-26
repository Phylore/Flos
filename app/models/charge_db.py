from database import db
from datetime import datetime

class Charge(db.Model):
    __tablename__ = "charge"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    angelegt_am = db.Column(db.DateTime, default=datetime.utcnow)
    lieferant_id = db.Column(db.Integer, db.ForeignKey("lieferant.id"))  # NEU
    geraete = db.relationship('Geraet', backref='charge', lazy=True)
    lieferant = db.relationship('Lieferant', back_populates='chargen')  # NEU

