from models.teil_db import *

# === Modul-Standards für Kategorie: Saugroboter ===

# Roboter: Nur Saugen
Saugroboter_Roboter_Standard1 = [
    HAUPTBÜRSTE,
    NEBENBÜRSTE,
    STAUBBEHÄLTER,
    STAUBFILTER
]

# Roboter: Saugen + Wischen (+ Wassertank im Roboter)
Saugroboter_Roboter_Standard2 = Saugroboter_Roboter_Standard1 + [
    WISCHPADHALTER,
    WASSERTANK_ROBOTER
]

# Station: Minimale Ladestation (nur Strom)
Saugroboter_Station_Standard1 = [
    STROMKABEL,
    BASIS
]

# Station: Große Station mit Tanks und Reinigung
Saugroboter_Station_Standard2 = Saugroboter_Station_Standard1 + [
    WASSERTANK,
    ABWASSERTANK,
    STAUBBEUTEL,
    RAMPE,
    WASCHMODUL
]

# === Modul-Standards für Kategorie: Stabsauger ===

# Einfacher Stabsauger
Stabsauger_Standard1 = [
    HAUPTBÜRSTE,
    STAUBBEHÄLTER,
    STAUBFILTER
]

# Erweiterter Stabsauger (z. B. Bespoke Jet)
Stabsauger_Standard2 = Stabsauger_Standard1 + [
    NEBENBÜRSTE
]

# Basisstation für Stabsauger
Stabsauger_Station_Standard1 = [
    BASIS,
    STROMKABEL
]

# Premiumstation (z. B. All-in-One Clean Station)
Stabsauger_Station_Standard2 = Stabsauger_Station_Standard1  # ggf. später erweitern

module_standards = {
    # Saugroboter
    "Saugroboter-Roboter-Standard1": Saugroboter_Roboter_Standard1,
    "Saugroboter-Roboter-Standard2": Saugroboter_Roboter_Standard2,
    "Saugroboter-Station-Standard1": Saugroboter_Station_Standard1,
    "Saugroboter-Station-Standard2": Saugroboter_Station_Standard2,

    # Stabsauger
    "Stabsauger-Standard1": Stabsauger_Standard1,
    "Stabsauger-Standard2": Stabsauger_Standard2,
    "Stabsauger-Station-Standard1": Stabsauger_Station_Standard1,
    "Stabsauger-Station-Standard2": Stabsauger_Station_Standard2
}

