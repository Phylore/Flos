from app.app import app, db

from models.benutzer_db import Benutzer
from models.zustand_db import Zustand
from models.modell_db import Modell
from models.kategorie_db import Kategorie
from models.geraet_db import Geraet

from app.setup.setup_modelle_import import import_modelle_wenn_notwendig

def init_zustaende():
    standardwerte = [
        ("Ja", "Anwesenheit"),
        ("Ersetzt", "Anwesenheit"),
        ("Nein", "Anwesenheit"),
        ("Nicht geprüft", "Anwesenheit"),
        ("1", "Sauberkeit"),
        ("2", "Sauberkeit"),
        ("3", "Sauberkeit"),
        ("4", "Sauberkeit"),
        ("5", "Sauberkeit"),
        ("Nicht bewertet", "Sauberkeit"),
        ("Ja", "Funktioniert"),
        ("Nein", "Funktioniert"),
        ("Unklar", "Funktioniert")
    ]

    for value, kategorie in standardwerte:
        if not Zustand.query.filter_by(value=value, kategorie=kategorie).first():
            db.session.add(Zustand(value=value, kategorie=kategorie))
    db.session.commit()
    print("✅ Zustände initialisiert.")

def init_benutzer():
    admin = Benutzer(name="admin", passwort_hash="admin", rolle="admin")
    eric = Benutzer(name="eric", passwort_hash="eric", rolle="user")
    max = Benutzer(name="max", passwort_hash="max", rolle="user")
    db.session.add_all([admin, eric, max])
    db.session.commit()
    print("✅ Benutzer 'admin', 'eric', 'max' wurden angelegt.")

def beispielgeraete_anlegen():
    admin = Benutzer.query.filter_by(name="admin").first()
    modell_l10 = Modell.query.filter_by(name="Dreame L10").first()
    modell_x40 = Modell.query.filter_by(name="Dreame X40").first()
    zustand = Zustand.query.filter_by(value="Ja", kategorie="Funktioniert").first()

    if not all([admin, modell_l10, modell_x40, zustand]):
        print("❌ Fehlende Objekte – kein Gerät angelegt.")
        return

    g1 = Geraet(qrcode="TEST-L10", modell=modell_l10, zustand=zustand, benutzer=admin)
    g2 = Geraet(qrcode="TEST-X40", modell=modell_x40, zustand=zustand, benutzer=admin)
    db.session.add_all([g1, g2])
    db.session.commit()
    print("✅ Beispielgeräte wurden angelegt.")

with app.app_context():
    db.drop_all()
    db.create_all()
    print("📦 Datenbanktabellen erstellt.")

    init_zustaende()
    init_benutzer()

    print("[SETUP] Prüfe, ob Modelle importiert werden müssen...")
    import_modelle_wenn_notwendig()

    beispielgeraete_anlegen()

