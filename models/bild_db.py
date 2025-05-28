from database import db

class GeraetBild(db.Model):
    __tablename__ = "geraet_bild"

    id = db.Column(db.Integer, primary_key=True)
    geraet_id = db.Column(db.Integer, db.ForeignKey("geraete.id"), nullable=False)
    pfad = db.Column(db.String(255), nullable=False)
    beschreibung = db.Column(db.String(100))

    def __repr__(self):
        return f"<Bild für Gerät {self.geraet_id}: {self.pfad}>"

