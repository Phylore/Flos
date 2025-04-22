
# Datei: initialisiere_teststruktur.py

from models.geraetetest_db import GeraeteTestSchritt
from database import db
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modelle.stabstaubsauger_modelle import stabstaubsauger_modelle
from models.test_defaults_db import test_standards

ALLE_MODELLE = {
    **saugroboter_modelle,
    **stabstaubsauger_modelle
}

def initialisiere_tests_fuer_geraet(geraet):
    modell_name = geraet.modell.name
    test_keys = ALLE_MODELLE.get(modell_name, {}).get("tests", [])

    hinzugefuegt = 0

    for key in test_keys:
        if key not in test_standards:
            print(f"❌ Kein Test-Standard gefunden für: {key}")
            continue

        for eintrag in test_standards[key]:
            name = eintrag.get("name")
            modul = eintrag.get("modul_name")
            if not name:
                print(f"⚠️ Fehlerhafte Testschritt-Vorlage – ohne Namen")
                continue

            vorhandener = GeraeteTestSchritt.query.filter_by(name=name).first()
            if not vorhandener:
                schritt = GeraeteTestSchritt(name=name, modul_name=modul)
                db.session.add(schritt)
                hinzugefuegt += 1

    if hinzugefuegt > 0:
        db.session.commit()
        print(f"✅ {hinzugefuegt} neue Testschritte für {modell_name} gespeichert.")
    else:
        print(f"ℹ️ Alle Testschritte für {modell_name} waren bereits vorhanden.")
