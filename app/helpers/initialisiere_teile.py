from app.models.zustand_db import Zustand
from database import db

def initialisiere_teile_fuer_geraet(geraet):
    """
    Diese Funktion wurde deaktiviert, da alle Geräte vollständig über die
    Definitionen in setup_modelle_import.py und saugroboter_modelle.py
    initialisiert werden.
    """
    print(f"ℹ️ Gerät {geraet.qrcode} wird über Modellstruktur initialisiert – keine automatische Teilzuweisung.")
