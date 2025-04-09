# test_geraete_anlegen.py

from app import app, db
from models.geraet_db import Geraet
from models.modell_db import Modell
from models.benutzer_db import Benutzer

with app.app_context():
    admin = Benutzer.query.get(1)
    if not admin:
        print("❌ Kein Benutzer mit ID 1 gefunden.")
        exit()

    l10 = Modell.query.filter_by(name="Dreame L10").first()
    x40 = Modell.query.filter_by(name="Dreame X40").first()

    if not l10 or not x40:
        print("❌ Modelle nicht gefunden.")
        exit()

    # Testgeräte anlegen
    geraet1 = Geraet(qrcode="DL10-TEST", modell_id=l10.id, benutzer_id=admin.id, zustand_id=1)
    geraet2 = Geraet(qrcode="X40-TEST", modell_id=x40.id, benutzer_id=admin.id, zustand_id=1)

    db.session.add_all([geraet1, geraet2])
    db.session.commit()
    print("✅ Testgeräte wurden erfolgreich angelegt.")

