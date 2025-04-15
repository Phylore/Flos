class TeilVorlage(db.Model):
    __tablename__ = "teilvorlage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    teile = db.relationship('Teil', backref='teilvorlage', lazy=True)

