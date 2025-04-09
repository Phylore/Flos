# init_db.py
from app.app import app
from database import db
from models import *
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.benutzer_db import Benutzer
from models.zustand_db import Zustand

def zustand_vorbefuellen():
    if not Zustand.query.first():
        standard_zustaende = ["unbekannt", "sehr gut", "gut", "okay", "miese", "defekt"]
        for name in standard_zustaende:
            db.session.add(Zustand(value=name))
        db.session.commit()
        print(f"✅ {len(standard_zustaende)} Zustände importiert.")
    else:
        print("ℹ️ Zustände bereits vorhanden.")

def benutzer_check_und_erstellen():
    def safe_create(name, klartext_passwort):
        user = Benutzer.query.filter_by(name=name).first()
        if not user:
            user = Benutzer(name=name)
            user.set_passwort(klartext_passwort)
            db.session.add(user)
            print(f"✅ Benutzer '{name}' wurde neu erstellt.")
        else:
            print(f"ℹ️ Benutzer '{name}' existiert bereits.")

    safe_create("admin", "admin")
    safe_create("eric", "eric")
    safe_create("max", "max")
    db.session.commit()

    print("👥 Benutzerprüfung abgeschlossen.\n")
    benutzer_liste = Benutzer.query.all()
    print(f"📋 Aktuell registrierte Benutzer ({len(benutzer_liste)}):")
    for benutzer in benutzer_liste:
        print(f" - {benutzer.name}")

with app.app_context():
    db.create_all()
    zustand_vorbefuellen()
    benutzer_check_und_erstellen()
    import_modelle_wenn_notwendig()

