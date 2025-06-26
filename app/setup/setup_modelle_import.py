import os
from app.models.modell_db import Modell
from app.models.kategorie_db import Kategorie
from app.models.modul_db import Modul
from app.models.teil_db import Teil
from app.models.zustand_db import Zustand
from database import db
from app.models.hersteller_db import Hersteller

# Modelldefinitionen
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modelle.stabstaubsauger_modelle import stabstaubsauger_modelle  # NEU
from models.modul_defaults_db import module_standards

# Alle Modell-Quellen kombinieren
ALLE_MODELLSAMMLUNGEN = [
    saugroboter_modelle,
    stabstaubsauger_modelle  # NEU
]

def zustand_by_kategorie(value, kategorie):
    with db.session.no_autoflush:
        return Zustand.query.filter_by(value=value, kategorie=kategorie).first()

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
            herstellername = eintrag.get("hersteller")

            hersteller = Hersteller.query.filter_by(name=herstellername).first()
            if not hersteller:
                print(f"[SKIP] Hersteller '{herstellername}' nicht gefunden – Modell '{modellname}' übersprungen.")
                continue

            kategorie = Kategorie.query.filter_by(name=kategoriename).first()
            if not kategorie:
                kategorie = Kategorie(name=kategoriename)
                db.session.add(kategorie)
                db.session.flush()

            modell = Modell(name=modellname, kategorie_id=kategorie.id, hersteller_id=hersteller.id)
            db.session.add(modell)
            print(f"[SETUP] Modell '{modellname}' ({herstellername}) zur Kategorie '{kategoriename}' hinzugefügt.")

            for modulname, modultyp in eintrag["module"].items():
                modul = Modul(name=modulname, modell=modell)

                def add_teile(typ):
                    teile_def = module_standards.get(typ, [])
                    for teil_vorlage in teile_def:
                        name = getattr(teil_vorlage, "name", str(teil_vorlage))
                        teil = Teil(
                            name=name,
                            anwesenheit=zustand_by_kategorie("vorhanden", "Anwesenheit"),
                            sauberkeit=zustand_by_kategorie("sauber", "Sauberkeit"),
                            beschaedigung=zustand_by_kategorie("intakt", "Beschädigung")
                        )
                        modul.teile.append(teil)

                if isinstance(modultyp, str):
                    add_teile(modultyp)
                elif isinstance(modultyp, list):
                    for typ in modultyp:
                        add_teile(typ)

                db.session.add(modul)

    db.session.commit()
    print("[SETUP] Modellimport abgeschlossen.")

