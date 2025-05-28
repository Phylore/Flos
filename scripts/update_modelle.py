# Datei: scripts/update_modelle.py
from app.app import app
from models.modell_db import Modell
from models.hersteller_db import Hersteller
from models.kategorie_db import Kategorie
from database import db

with app.app_context():
    dreame = Hersteller.query.filter_by(name="Dreame").first()
    if not dreame:
        dreame = Hersteller(name="Dreame")
        db.session.add(dreame)
        db.session.commit()

    kat = Kategorie.query.filter_by(name="Saugroboter").first()
    if not kat:
        raise Exception("Kategorie 'Saugroboter' fehlt")

    if not Modell.query.filter_by(name="Dreame D10 Plus").first():
        m = Modell(name="Dreame D10 Plus", hersteller_id=dreame.id, kategorie_id=kat.id)
        db.session.add(m)
        db.session.commit()
        print("Modell hinzugefügt.")
    else:
        print("Modell bereits vorhanden.")

