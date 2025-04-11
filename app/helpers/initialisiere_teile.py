from models.teil_db import alle_teilvorlagen  # korrekt importieren
from models.modul_db import Modul
from models.teil_db import Teil
from models.zustand_db import Zustand
from database import db

def initialisiere_teile_fuer_geraet(geraet):
    """
    Erstellt Module und Teile für ein neues Gerät – inklusive Zubehörmodul.
    """
    zustaende = Zustand.query.all()
    standard_zustand = next((z for z in zustaende if z.name.lower() == "okay"), zustaende[0])

    # Beispielmodul hinzufügen
    roboter_modul = Modul(name="Roboter", geraet=geraet)
    for vorlage in alle_teilvorlagen:
        if "Saugroboter" in vorlage.kategorien:
            roboter_modul.teile.append(
                Teil(name=vorlage.name, zustand=standard_zustand, geraet=geraet)
            )
    db.session.add(roboter_modul)

    # Zubehörmodul
    zubehoer_modul = Modul(name="Zubehör", geraet=geraet)
    for name in ["Karton", "Ersatzfilter", "Anleitung"]:
        zubehoer_modul.teile.append(
            Teil(name=name, zustand=standard_zustand, geraet=geraet)
        )
    db.session.add(zubehoer_modul)

    db.session.commit()

