
from app.app import app
from database import db
from models.modell_db import Modell
from models.modul_db import Modul
from models.teil_db import Teil
from models.zustand_db import Zustand

with app.app_context():
    modell = Modell.query.filter_by(name="Dreame L10").first()
    if not modell:
        print("❌ Modell 'Dreame L10' nicht gefunden.")
    else:
        print(f"✅ Modell gefunden: {modell.name}")
        
        if modell.module:
            print(f"ℹ️ Modell hat bereits {len(modell.module)} Modul(e). Kein Fix nötig.")
        else:
            zustand_standard = Zustand.query.first()
            if not zustand_standard:
                print("❌ Kein Zustand gefunden – bitte zuerst Zustaende importieren.")
            else:
                # Modul + 2 Teile erzeugen
                station = Modul(name="Station", modell_id=modell.id)
                teil1 = Teil(name="Basis", zustand=zustand_standard)
                teil2 = Teil(name="Sensor", zustand=zustand_standard)
                station.teile.extend([teil1, teil2])

                db.session.add(station)
                db.session.commit()
                print("✅ Modul 'Station' mit 2 Teilen wurde erfolgreich angelegt.")
