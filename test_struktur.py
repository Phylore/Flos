from app.app import app, db
from models.geraet_db import Geraet

with app.app_context():
    geraete = Geraet.query.all()
    print(f"Gefundene Geräte: {len(geraete)}\n")

    for g in geraete:
        print(f"🔧 Gerät: {g.qrcode}")
        print(f"  Module: {len(g.modul_liste)}")

        for m in g.modul_liste:
            print(f"    📦 Modul: {m.name}")
            print(f"      Teile: {len(m.teile)}")
            for t in m.teile:
                print(f"        - Teil: {t.name} (anwesenheit_id: {t.anwesenheit_id})")

        print("-" * 40)

