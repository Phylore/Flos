
from models.geraetetest_db import GeraeteTestDurchlauf, GeraeteTestErgebnis, GeraeteTestSchritt
from database import db
from flask_login import current_user
from models.test_defaults_db import test_standards
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modelle.stabstaubsauger_modelle import stabstaubsauger_modelle

ALLE_MODELLE = {
    **saugroboter_modelle,
    **stabstaubsauger_modelle
}

def initialisiere_testdurchlauf(geraet, benutzer=None):
    benutzer_id = benutzer.id if benutzer else current_user.id

    modell_name = geraet.modell.name
    test_keys = ALLE_MODELLE.get(modell_name, {}).get("tests", [])

    durchlauf = GeraeteTestDurchlauf(geraet_id=geraet.id, benutzer_id=benutzer_id)
    db.session.add(durchlauf)
    db.session.flush()

    angelegt = 0

    for key in test_keys:
        for eintrag in test_standards.get(key, []):
            schritt = GeraeteTestSchritt.query.filter_by(name=eintrag["name"]).first()
            if not schritt:
                continue

            ergebnis = GeraeteTestErgebnis(
                durchlauf_id=durchlauf.id,
                schritt_id=schritt.id,
                bestanden=None,
                kommentar=""
            )
            db.session.add(ergebnis)
            angelegt += 1

    db.session.commit()
    print(f"✅ Testdurchlauf mit {angelegt} Einträgen für '{modell_name}' angelegt.")
