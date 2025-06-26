from app import db

class Charge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    angelegt_am = db.Column(db.DateTime, default=datetime.utcnow)
    geraete = db.relationship('Geraet', backref='charge', lazy=True)

