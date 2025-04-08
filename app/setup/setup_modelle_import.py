import os
from models.modell_db import Modell
from models.kategorie_db import Kategorie
from database import db

# Importiere gezielt alle Modell-Definitionen (z. B. aus modelle/)
from models.modelle.saugroboter_modelle import saugroboter_modelle

# Liste aller Modellquellen
ALLE_MODELLSAMMLUNGEN = [
    saugroboter_modelle
    # Weitere Modellquellen wie staubsauger_modelle usw. hier ergänzen
]

def import_modelle_wenn_notwendig():
    print("[SETUP] Prüfe, ob Modelle importiert werden müssen...")

    bereits_vorhanden = Modell.query.count()
    if bereits_vorhanden > 0:
        print(f"[SETUP] {bereits_vorhanden} Modelle bereits vorhanden. Kein Import nötig.")
        return

    print("[SETUP] Keine Modelle in DB gefunden – beginne Import...")

    for modellquelle in ALLE_MODELLSAMMLUNGEN:
        for modellname, eintrag in modellquelle.items():
            kategoriename = eintrag["kategorie"]

            # Kategorie holen oder erstellen
            kategorie = Kategorie.query.filter_by(name=kategoriename).first()
            if not kategorie:
                kategorie = Kategorie(name=kategoriename)
                db.session.add(kategorie)
                db.session.flush()  # um kategorie.id direkt zu bekommen

            # Modell prüfen oder anlegen
            modell = Modell.query.filter_by(name=modellname).first()
            if not modell:
                modell = Modell(name=modellname, kategorie_id=kategorie.id)
                db.session.add(modell)
                print(f"[SETUP] Modell '{modellname}' zur Kategorie '{kategoriename}' hinzugefügt.")

    db.session.commit()
    print("[SETUP] Modellimport abgeschlossen.")

