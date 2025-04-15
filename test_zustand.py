from app.app import app
from models.geraet_db import Geraet
from models.zustand_db import Zustand

with app.app_context():
    geraete = Geraet.query.all()
    print(f"Gefundene Geräte: {len(geraete)}\n")

    for g in geraete:
        print(f"🔧 Gerät: {g.qrcode}")
        print(f"  zustand_id: {g.zustand_id}")

        if g.zustand:
            print(f"  Zustand-Objekt gefunden: ✅")
            print(f"    → value: {getattr(g.zustand, 'value', '❌ value fehlt')}")
            print(f"    → id:    {g.zustand.id}")
        else:
            print(f"  Zustand: ❌ NICHT gesetzt")

        print("-" * 40)

