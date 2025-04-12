import os
from models.modell_db import Modell
from models.kategorie_db import Kategorie
from models.modul_db import Modul
from models.teil_db import Teil
from models.zustand_db import Zustand
from database import db

# Modelldefinitionen
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modul_defaults_db import module_standards

ALLE_MODELLSAMMLUNGEN = [
    saugroboter_modelle
    # weitere Modellquellen hier eintragen
]

def zustand_by_kategorie(value, kategorie):
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

            # Kategorie holen oder erstellen
            kategorie = Kategorie.query.filter_by(name=kategoriename).first()
            if not kategorie:
                kategorie = Kategorie(name=kategoriename)
                db.session.add(kategorie)
                db.session.flush()

            # Modell anlegen
            modell = Modell(name=modellname, kategorie_id=kategorie.id)
            db.session.add(modell)
            print(f"[SETUP] Modell '{modellname}' zur Kategorie '{kategoriename}' hinzugefügt.")

            # Module anlegen
            for modulname, modultyp in eintrag["module"].items():
                modul = Modul(name=modulname, modell=modell)

                # Modultyp (z. B. "Saugroboter-Station-Standard1") auflösen
                if isinstance(modultyp, str):
                    teile_def = module_standards.get(modultyp, [])
                    for teil_vorlage in teile_def:
                        name = teil_vorlage.name if hasattr(teil_vorlage, "name") else str(teil_vorlage)
                        teil = Teil(
                            name=name,
                            anwesenheit=zustand_by_kategorie("vorhanden", "Anwesenheit"),
                            sauberkeit=zustand_by_kategorie("sauber", "Sauberkeit"),
                            beschaedigung=zustand_by_kategorie("intakt", "Beschädigung")
                        )
                        modul.teile.append(teil)
                elif isinstance(modultyp, list):
                    for typ in modultyp:
                        teile_def = module_standards.get(typ, [])
                        for teil_vorlage in teile_def:
                            name = teil_vorlage.name if hasattr(teil_vorlage, "name") else str(teil_vorlage)
                            teil = Teil(
                                name=name,
                                anwesenheit=zustand_by_kategorie("vorhanden", "Anwesenheit"),
                                sauberkeit=zustand_by_kategorie("sauber", "Sauberkeit"),
                                beschaedigung=zustand_by_kategorie("intakt", "Beschädigung")
                            )
                            modul.teile.append(teil)

                db.session.add(modul)

    db.session.commit()
    print("[SETUP] Modellimport abgeschlossen.")
