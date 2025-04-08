from models.teil_db import *

# === Modul-Standards für Kategorie: Saugroboter ===

Saugroboter_Station_Standard1 = [
    STROMKABEL, 
    WASSERTANK, 
    ABWASSERTANK, 
    STAUBBEUTEL,
    BASIS,
    RAMPE,
    WASCHMODUL
]

Saugroboter_Roboter_Standard1 = [
    HAUPTBÜRSTE,
    NEBENBÜRSTE,
    WISCHPADHALTER,
    WISCHPADS,
    STAUBBEHÄLTER,
    STAUBFILTER
]

module_standards = {
    "Saugroboter-Station-Standard1": Saugroboter_Station_Standard1,
    "Saugroboter-Roboter-Standard1": Saugroboter_Roboter_Standard1
}

