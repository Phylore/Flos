# app/models/modelle/saugroboter/saugroboter_teile_seed.py

# Hier pflegst du deine Standardteile (nur für den Import, danach ist die DB der "Single Source of Truth")

saugroboter_teile = [
    {"name": "Stromkabel",      "typ": "Kabel",   "modul": "Station"},
    {"name": "Wassertank",      "typ": "Tank",    "modul": "Station"},
    {"name": "Abwassertank",    "typ": "Tank",    "modul": "Station"},
    {"name": "Staubbeutel",     "typ": "Beutel",  "modul": "Station"},
    {"name": "Basis",           "typ": "Basis",   "modul": "Station"},
    {"name": "Rampe",           "typ": "Rampe",   "modul": "Station"},
    {"name": "Waschmodul",      "typ": "Modul",   "modul": "Station"},
    {"name": "Hauptbürste",     "typ": "Bürste",  "modul": "Roboter"},
    {"name": "Seitenbürste",    "typ": "Bürste",  "modul": "Roboter"},
    {"name": "Nebenbürste",     "typ": "Bürste",  "modul": "Roboter"},
    {"name": "Staubbehälter",   "typ": "Behälter","modul": "Roboter"},
    {"name": "Staubfilter",     "typ": "Filter",  "modul": "Roboter"},
    {"name": "Wischpadhalter",  "typ": "Halter",  "modul": "Roboter"},
    {"name": "Wischstoff",      "typ": "Textil",  "modul": "Roboter"},
    {"name": "Wassertank (Roboter)", "typ": "Tank", "modul": "Roboter"}
]

