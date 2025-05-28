import sys
sys.path.append("models/modelle")

from database import db
from models.hersteller_db import Hersteller
from models.kategorie_db import Kategorie, Unterkategorie
from models.modell_db import Modell
from saugroboter_modelle import saugroboter_modelle
from app import app

with app.app_context():
    Modell.query.delete()
    db.session.commit()

    for modell_name, daten in saugroboter_modelle.items():
        hersteller = Hersteller.query.filter_by(name=daten["hersteller"]).first()
        kategorie = Kategorie.query.filter_by(name=daten["kategorie"]).first()

        if not hersteller or not kategorie:
            print(f"⚠️ {modell_name}: Hersteller oder Kategorie nicht gefunden")
            continue

        uk_name = daten["unterkategorie"].strip()
        unterkategorie = Unterkategorie.query.filter_by(name=uk_name, kategorie_id=kategorie.id).first()

        if not unterkategorie:
            print(f"⚠️ {modell_name}: Unterkategorie '{uk_name}' nicht gefunden")
            continue

        modell = Modell(
            name=modell_name,
            hersteller_id=hersteller.id,
            kategorie_id=kategorie.id,
            unterkategorie_id=unterkategorie.id
        )
        db.session.add(modell)

    db.session.commit()
    print("✅ Modelle erfolgreich eingetragen.")

