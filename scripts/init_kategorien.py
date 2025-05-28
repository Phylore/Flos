from database import db
from models.kategorie_db import Kategorie, Unterkategorie
from app import app

KATEGORIEN = {
    "Staubsauger": [
        "Normaler Staubsauger",
        "Stabsauger",
        "Wischsauger"
    ],
    "Saugroboter": [
        "Mit Station, Mit Wischfunktion",
        "Mit Station, Ohne Wischfunktion",
        "Ohne Station, Mit Wischfunktion",
        "Ohne Station, Ohne Wischfunktion"
    ],
    "Kaffeemaschine": [
        "Filterkaffee",
        "Kapsel",
        "Vollautomat",
        "Siebträger",
        "Padmaschine"
    ],
    "Küchengeräte": [
        "Fritteuse",
        "Heißluftfritteuse",
        "Mikrowelle",
        "Backofen"
    ]
}

with app.app_context():
    db.session.query(Unterkategorie).delete()
    db.session.query(Kategorie).delete()
    db.session.commit()

    for kat_name, ukats in KATEGORIEN.items():
        kat = Kategorie(name=kat_name)
        db.session.add(kat)
        db.session.flush()  # holt kat.id

        for uk in ukats:
            db.session.add(Unterkategorie(name=uk, kategorie_id=kat.id))

    db.session.commit()
    print("Kategorien + Unterkategorien erfolgreich eingetragen.")

