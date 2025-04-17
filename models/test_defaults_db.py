# KEIN Import von GeraeteTestSchritt hier – nur Daten

Funktionstest_Standard1 = [
    {"name": "Gerät geht an", "modul_name": "Roboter"},
    {"name": "Verbindet sich", "modul_name": "Roboter"},
    {"name": "Lädt", "modul_name": "Roboter"},
    {"name": "Findet heim", "modul_name": "Roboter"},
    {"name": "Saugt", "modul_name": "Roboter"},
    {"name": "Station geht an", "modul_name": "Station"},
    {"name": "Gibt Signal", "modul_name": "Station"},
    {"name": "Lädt Roboter", "modul_name": "Station"},
    {"name": "Selbstreinigung", "modul_name": "Station"},
    {"name": "Absaugen", "modul_name": "Station"},
]

Funktionstest_Standard2 = Funktionstest_Standard1 + [
    {"name": "Wischt", "modul_name": "Roboter"},
    {"name": "Gibt Wasser", "modul_name": "Roboter"},
    {"name": "Wasserzulauf", "modul_name": "Station"},
    {"name": "Wasser abpumpen", "modul_name": "Station"},
]

test_standards = {
    "Funktionstest-Standard1": Funktionstest_Standard1,
    "Funktionstest-Standard2": Funktionstest_Standard2,
}

