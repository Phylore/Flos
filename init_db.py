from app.app import app, db

from models.benutzer_db import Benutzer
from models.zustand_db import Zustand, STANDARD_ZUSTAENDE
from models.modell_db import Modell
from models.kategorie_db import Kategorie
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from app.setup.init_hersteller import init_hersteller

def init_zustaende():
    for kategorie, werte in STANDARD_ZUSTAENDE.items():
        for value in werte:
            if not Zustand.query.filter_by(value=value, kategorie=kategorie).first():
                db.session.add(Zustand(value=value, kategorie=kategorie))
    db.session.commit()
    print("✅ Zustände initialisiert.")

def init_benutzer():
    admin = Benutzer(name="admin", rolle="admin")
    admin.set_passwort("admin")

    alper = Benutzer(name="alper", rolle="user")
    alper.set_passwort("alper1")

    moritz = Benutzer(name="moritz", rolle="user")
    moritz.set_passwort("moritz1")

    eric = Benutzer(name="eric", rolle="user")
    eric.set_passwort("eric")

    batu = Benutzer(name="batu", rolle="user")
    batu.set_passwort("batu")

    jesse = Benutzer(name="jesse", rolle="user")
    jesse.set_passwort("jesse")

    db.session.add_all([admin, eric, alper, moritz, batu, jesse])
    db.session.commit()
    print("✅ Benutzer wurden angelegt.")

with app.app_context():
    db.drop_all()
    db.create_all()
    print("📦 Datenbanktabellen erstellt.")

    init_zustaende()
    init_benutzer()

    init_hersteller()
    print("[SETUP] Prüfe, ob Modelle importiert werden müssen...")
    import_modelle_wenn_notwendig()

    print("✅ Setup abgeschlossen.")

