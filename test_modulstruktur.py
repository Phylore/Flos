
from app.app import app
from database import db
from models.geraet_db import Geraet
from flask import url_for

with app.app_context():
    geraet = Geraet.query.first()
    if not geraet:
        print("❌ Kein Gerät gefunden.")
    else:
        print(f"✅ Gerät gefunden: QR-Code = {geraet.qrcode}")
        print(f"Modell: {geraet.modell.name if geraet.modell else '❌ Kein Modell'}")

        module = geraet.modell.module if geraet.modell else []
        print(f"Module: {len(module)} gefunden")

        for modul in module:
            print(f" - Modul: {modul.name} ({len(modul.teile)} Teile)")
            for teil in modul.teile:
                zustand = teil.zustand.value if teil.zustand else "unbekannt"
                print(f"   • Teil: {teil.name} – Zustand: {zustand}")
