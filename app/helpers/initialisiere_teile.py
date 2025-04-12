from models.teil_db import alle_teilvorlagen  # korrekt importieren
from models.modul_db import Modul
from models.teil_db import Teil
from models.zustand_db import Zustand
from database import db

def zustand_by_kategorie(value, kategorie):
    return Zustand.query.filter_by(value=value, kategorie=kategorie).first()

def initialisiere_teile_fuer_geraet(geraet):
    """
    Erstellt Module und Teile für ein neues Gerät – inklusive Zubehörmodul.
    """

    # Standardzustände holen
    anwesenheit = zustand_by_kategorie("vorhanden", "Anwesenheit")
    sauberkeit = zustand_by_kategorie("sauber", "Sauberkeit")
    beschaedigung = zustand_by_kategorie("intakt", "Beschädigung")

    # Beispielmodul hinzufügen
    roboter_modul = Modul(name="Roboter", geraet=geraet)
    for vorlage in alle_teilvorlagen:
        if "Saugroboter" in vorlage.kategorien:
            roboter_modul.teile.append(
                Teil(
                    name=vorlage.name,
                    geraet=geraet,
                    anwesenheit=anwesenheit,
                    sauberkeit=sauberkeit,
                    beschaedigung=beschaedigung
                )
            )
    db.session.add(roboter_modul)

    # Zubehörmodul
    zubehoer_modul = Modul(name="Zubehör", geraet=geraet)
    for name in ["Karton", "Ersatzfilter", "Anleitung"]:
        zubehoer_modul.teile.append(
            Teil(
                name=name,
                geraet=geraet,
                anwesenheit=anwesenheit,
                sauberkeit=sauberkeit,
                beschaedigung=beschaedigung
            )
        )
    db.session.add(zubehoer_modul)

    db.session.commit()
