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

module_standards = {
    "Saugroboter-Roboter-Standard1": Saugroboter_Roboter_Standard1,
    "Saugroboter-Roboter-Standard2": Saugroboter_Roboter_Standard2,
    "Saugroboter-Station-Standard1": Saugroboter_Station_Standard1,
    "Saugroboter-Station-Standard2": Saugroboter_Station_Standard2
}

