from app.app import app
from database import db
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig
from models.teil_db import Teil

# Importiere explizit alle Models, damit sie sicher registriert werden
from models import modul_db, teil_db, modell_db, kategorie_db

with app.app_context():
    print("=== SETUP START ===")
    print("[DEBUG] Registrierte Tabellen vor create_all():")
    print(list(db.metadata.tables.keys()))

    print("[SETUP] Erzeuge Tabellen falls nötig...")
    db.create_all()

    print("[DEBUG] Registrierte Tabellen nach create_all():")
    print(list(db.metadata.tables.keys()))

    print("[SETUP] Prüfe, ob Modelle importiert werden müssen...")
    import_modelle_wenn_notwendig()

    print("=== SETUP ENDE ===")

