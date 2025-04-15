from database import db  # Füge diesen Import hinzu

class TeilVorlage(db.Model):
    __tablename__ = "teilvorlage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    vorlage_teile = db.relationship('Teil', backref='vorlage_teile', lazy=True)  # Ändere den Backref-Namen

