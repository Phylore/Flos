# Datei: models/ersatzteil_defaults_db.py

# Nur Namen speichern → DB-Objekte erst bei Bedarf laden
ersatzteil_set_namen = {
    "Saugroboter-Ersatzteile-Standard1": [
        "Staubbeutel",
        "Seitenbürste",
        "Filter für Staubbeutel",
        "Wischpad", "Wischpad", "Wischpad", "Wischpad"
    ],
    "Ersatzbox-Premium": [
        "Staubbeutel", "Staubbeutel",
        "Seitenbürste", "Seitenbürste",
        "Filter für Staubbeutel", "Filter für Staubbeutel",
        "Wischpad", "Wischpad", "Wischpad", "Wischpad"
    ],
    "Saugroboter-Ersatzteile-Klein": [  # ✅ NEU hinzugefügt
        "Staubbeutel",
        "Seitenbürste",
        "Filter für Staubbeutel"
        # Keine Wischpads enthalten
    ]
}

def lade_vorlagen(namen_liste):
    from models.teilvorlage_db import TeilVorlage
    return [TeilVorlage.query.filter_by(name=name).first() for name in namen_liste]

