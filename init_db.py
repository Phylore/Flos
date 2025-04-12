# init_db.py
from app.app import app
from database import db
from models import *
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.benutzer_db import Benutzer
from models.zustand_db import Zustand

def zustand_vorbefuellen():
    if not Zustand.query.first():
        zustaende = [
            # Anwesenheit
            ("Ja", "Anwesenheit"),
            ("Ersetzt", "Anwesenheit"),
            ("Nein", "Anwesenheit"),

            # Sauberkeit (1–5, 5 = sehr sauber)
            ("5 – sehr sauber", "Sauberkeit"),
            ("4 – sauber", "Sauberkeit"),
            ("3 – mittel", "Sauberkeit"),
            ("2 – schmutzig", "Sauberkeit"),
            ("1 – sehr schmutzig", "Sauberkeit"),

            # Funktionalität
            ("Ja", "Funktioniert"),
            ("Nein", "Funktioniert"),
            ("Unklar", "Funktioniert"),
        ]
        for value, kategorie in zustaende:
            db.session.add(Zustand(value=value, kategorie=kategorie))
        db.session.commit()
        print(f"✅ {len(zustaende)} neue differenzierte Zustände importiert.")
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

    print("👥 Benutzerprüfung abgeschlossen.")
    benutzer_liste = Benutzer.query.all()
    print(f"📋 Aktuell registrierte Benutzer ({len(benutzer_liste)}):")
    for benutzer in benutzer_liste:
        print(f" - {benutzer.name}")

with app.app_context():
    db.create_all()
    zustand_vorbefuellen()
    benutzer_check_und_erstellen()
    import_modelle_wenn_notwendig()
