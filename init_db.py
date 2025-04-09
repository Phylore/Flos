# init_db.py
from app.app import app
from database import db
from models import *  # Registriert alle Tabellen sauber
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.benutzer_db import Benutzer

def benutzer_check():
    benutzer_liste = Benutzer.query.all()
    if not benutzer_liste:
        print("⚠️  Achtung: Keine Benutzer in der Datenbank vorhanden!")
    else:
        print(f"✅ {len(benutzer_liste)} Benutzer erfolgreich geladen:")
        for benutzer in benutzer_liste:
            print(f" - {benutzer.name}")

with app.app_context():
    db.create_all()
    import_modelle_wenn_notwendig()
    benutzer_check()

