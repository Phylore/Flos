import importlib.util
import os

pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/models/modelle/saugroboter/saugroboter_modelle.py'))
spec = importlib.util.spec_from_file_location("saugroboter_modelle", pfad)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
saugroboter_modelle = mod.saugroboter_modelle  # Jetzt ist das Dict verfügbar!

from app import app
from database import db
from app.models.kategorie_db import Kategorie, Unterkategorie
from app.models.hersteller_db import Hersteller
from app.models.modell_db import Modell


def get_or_create(model, **kwargs):
    """Holt den Eintrag oder legt ihn an, falls noch nicht vorhanden."""
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    db.session.add(instance)
    db.session.commit()
    return instance

with app.app_context():
    for modellname, daten in saugroboter_modelle.items():
        # Kategorie holen/erstellen
        kategorie = get_or_create(Kategorie, name=daten["kategorie"])

        # Hersteller holen/erstellen
        hersteller = get_or_create(Hersteller, name=daten["hersteller"])

        # Unterkategorie holen/erstellen (unique: Name + Kategorie)
        unterkategorie = Unterkategorie.query.filter_by(
            name=daten["unterkategorie"], kategorie_id=kategorie.id
        ).first()
        if not unterkategorie:
            unterkategorie = Unterkategorie(
                name=daten["unterkategorie"],
                kategorie_id=kategorie.id
            )
            db.session.add(unterkategorie)
            db.session.commit()

        # Modell prüfen/erstellen
        modell = Modell.query.filter_by(name=modellname).first()
        if not modell:
            modell = Modell(
                name=modellname,
                hersteller_id=hersteller.id,
                kategorie_id=kategorie.id,
                unterkategorie_id=unterkategorie.id
            )
            db.session.add(modell)
            db.session.commit()
            print(f"Modell '{modellname}' importiert.")
        else:
            print(f"Modell '{modellname}' existiert bereits.")

    print("Import abgeschlossen.")

