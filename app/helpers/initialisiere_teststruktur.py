# Datei: initialisiere_teststruktur.py

from models.geraetetest_db import GeraeteTestSchritt
from database import db
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.test_defaults_db import test_standards

def initialisiere_tests_fuer_geraet(geraet):
    modell_name = geraet.modell.name
    test_keys = saugroboter_modelle.get(modell_name, {}).get("tests", [])

    hinzugefuegt = 0

    for key in test_keys:
        if key not in test_standards:
            print(f"❌ Kein Test-Standard gefunden für: {key}")
            continue

        for vorlage in test_standards[key]:
            # Schritt nur einfügen, wenn er noch nicht existiert (nach Name)
            vorhandener = GeraeteTestSchritt.query.filter_by(name=vorlage.name).first()
            if not vorhandener:
                db.session.add(vorlage)
                hinzugefuegt += 1

    if hinzugefuegt > 0:
        db.session.commit()
        print(f"✅ {hinzugefuegt} neue Testschritte für {modell_name} gespeichert.")
    else:
        print(f"ℹ️ Alle Testschritte für {modell_name} waren bereits vorhanden.")

