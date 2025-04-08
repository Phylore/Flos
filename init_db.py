# init_db.py
from app.app import app
from database import db
from models.geraet_db import Geraet
from models.kategorie_db import Kategorie
from models.modell_db import Modell
from models.benutzer_db import Benutzer
from models.historie_db import Historie

with app.app_context():
    # Kategorien prüfen
    if not Kategorie.query.filter_by(name="Saugroboter").first():
        print("📦 Lege Kategorie 'Saugroboter' an...")
        sauger = Kategorie(name="Saugroboter")
        db.session.add(sauger)
        db.session.commit()

        print("🔧 Lege Modelle an...")
        m1 = Modell(name="Dreame L10", kategorie_id=sauger.id)
        m2 = Modell(name="Dreame X40", kategorie_id=sauger.id)

        db.session.add_all([m1, m2])
        db.session.commit()

        print("✅ Kategorie + Modelle erfolgreich angelegt.")
    else:
        print("✔️ Kategorie 'Saugroboter' existiert bereits – keine Änderungen vorgenommen.")

