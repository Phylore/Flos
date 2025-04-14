from database import db
from models.benutzer_db import Benutzer
from models.kategorie_db import Kategorie
from models.modell_db import Modell
from models.geraet_db import Geraet
from setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.zustand_db import Zustand

def zustand_vorbefuellen():
    if Zustand.query.count() == 0:
        standardwerte = [
            ("Ja", "Anwesenheit"), ("Ersetzt", "Anwesenheit"), ("Nein", "Anwesenheit"),
            ("Nicht geprüft", "Anwesenheit"),
            ("1", "Sauberkeit"), ("2", "Sauberkeit"), ("3", "Sauberkeit"),
            ("4", "Sauberkeit"), ("5", "Sauberkeit"), ("Nicht bewertet", "Sauberkeit"),
            ("Ja", "Funktioniert"), ("Nein", "Funktioniert"), ("Unklar", "Funktioniert")
        ]
        for value, kategorie in standardwerte:
            db.session.add(Zustand(value=value, kategorie=kategorie))
        db.session.commit()
        print(f"✅ {len(standardwerte)} neue differenzierte Zustände importiert.")
    else:
        print("ℹ️ Zustände bereits vorhanden.")

def beispielgeraete_anlegen():
    if not Geraet.query.first():
        admin = Benutzer.query.filter_by(name="admin").first()
        l10 = Modell.query.filter_by(name="Dreame L10").first()
        x40 = Modell.query.filter_by(name="Dreame X40").first()

        if admin and l10 and x40:
            db.session.add(Geraet(qrcode="TEST-L10", modell=l10, benutzer_id=admin.id))
            db.session.add(Geraet(qrcode="TEST-X40", modell=x40, benutzer_id=admin.id))
            db.session.commit()
            print("✅ Beispielgeräte angelegt.")
        else:
            print("❌ Modelle oder Admin nicht gefunden – keine Geräte angelegt.")
    else:
        print("ℹ️ Bereits Geräte vorhanden – keine neuen angelegt.")

def benutzer_anlegen():
    namen = ["admin", "eric", "max"]
    for name in namen:
        if not Benutzer.query.filter_by(name=name).first():
            user = Benutzer(name=name)
            user.set_passwort("test")
            if name == "admin":
                user.rolle = "admin"
            db.session.add(user)
    db.session.commit()
    print("✅ Benutzer 'admin', 'eric', 'max' wurden angelegt.")

def full_setup():
    db.create_all()
    zustand_vorbefuellen()
    benutzer_anlegen()
    import_modelle_wenn_notwendig()
    beispielgeraete_anlegen()

if __name__ == "__main__":
    from app.app import app
    with app.app_context():
        full_setup()