# init_db.py
from app.app import app
from database import db
from models import *
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.benutzer_db import Benutzer

def benutzer_anlegen():
    if Benutzer.query.count() == 0:
        users = [
            ("admin", "admin"),
            ("eric", "eric"),
            ("max", "max")
        ]
        for name, pw in users:
            user = Benutzer(name=name)
            user.set_passwort(pw)
            db.session.add(user)
        db.session.commit()
        print("✅ Benutzer 'admin', 'eric' und 'max' wurden neu angelegt.")
    else:
        print("ℹ️ Benutzer bereits vorhanden – kein neuer Eintrag.")

with app.app_context():
    db.create_all()
    import_modelle_wenn_notwendig()
    benutzer_anlegen()

