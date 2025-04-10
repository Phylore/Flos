# /app/helpers/initialisiere_teile.py

from models.teil_db import Teil, TeilVorlage
from models.zustand_db import Zustand
from database import db

def initialisiere_teile_fuer_geraet(geraet):
    """
    Erstellt zu einem Gerät alle passenden Teile (basierend auf Kategorie) mit Standardzustand.
    """
    if not geraet.modell or not geraet.modell.kategorie:
        raise ValueError("Modell oder Kategorie fehlen beim Gerät.")

    kategorie_name = geraet.modell.kategorie.name
    teilvorlagen = TeilVorlage.query.all()
    zustaende = Zustand.query.all()

    standard_zustand = next((z for z in zustaende if z.name.lower() == "okay"), None)
    if not standard_zustand:
        raise ValueError("Standardzustand 'okay' nicht in der Datenbank gefunden.")

    for vorlage in teilvorlagen:
        if kategorie_name in vorlage.kategorien:
            teil = Teil(
                geraet_id=geraet.id,
                teil_vorlage_id=vorlage.id,
                zustand_id=standard_zustand.id
            )
            db.session.add(teil)

    db.session.commit()

