# app/models/modelle/saugroboter/saugroboter_modul_defaults_db.py

# === Modul-Standards für Kategorie: Saugroboter ===

# Roboter: Nur Saugen
Saugroboter_Roboter_Standard1 = [
    "Hauptbürste",
    "Nebenbürste",
    "Staubbehälter",
    "Staubfilter"
]

# Roboter: Saugen + Wischen (+ Wassertank im Roboter)
Saugroboter_Roboter_Standard2 = Saugroboter_Roboter_Standard1 + [
    "Wischpadhalter",
    "Wassertank (Roboter)"
]

# Station: Minimale Ladestation (nur Strom)
Saugroboter_Station_Standard1 = [
    "Stromkabel",
    "Basis"
]

# Station: Große Station mit Tanks und Reinigung
Saugroboter_Station_Standard2 = Saugroboter_Station_Standard1 + [
    "Wassertank",
    "Abwassertank",
    "Staubbeutel",
    "Rampe",
    "Waschmodul"
]

module_standards = {
    "Saugroboter-Roboter-Standard1": Saugroboter_Roboter_Standard1,
    "Saugroboter-Roboter-Standard2": Saugroboter_Roboter_Standard2,
    "Saugroboter-Station-Standard1": Saugroboter_Station_Standard1,
    "Saugroboter-Station-Standard2": Saugroboter_Station_Standard2
}
