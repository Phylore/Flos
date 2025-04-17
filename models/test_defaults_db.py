from models.geraetetest_db import GeraeteTestSchritt

# Roboter-Schritte
GEHT_AN = GeraeteTestSchritt(name="Gerät geht an", modul_name="Roboter")
VERBINDET_SICH = GeraeteTestSchritt(name="Verbindet sich", modul_name="Roboter")
LAEDT = GeraeteTestSchritt(name="Lädt", modul_name="Roboter")
FINDET_HEIM = GeraeteTestSchritt(name="Findet heim", modul_name="Roboter")
SAUGT = GeraeteTestSchritt(name="Saugt", modul_name="Roboter")
WISCHT = GeraeteTestSchritt(name="Wischt", modul_name="Roboter")
GIBT_WASSER = GeraeteTestSchritt(name="Gibt Wasser", modul_name="Roboter")

# Station-Schritte
STATION_GEHT_AN = GeraeteTestSchritt(name="Station geht an", modul_name="Station")
SIGNAL = GeraeteTestSchritt(name="Gibt Signal", modul_name="Station")
LAEDT_ROBOTER = GeraeteTestSchritt(name="Lädt Roboter", modul_name="Station")
REINIGUNG = GeraeteTestSchritt(name="Selbstreinigung", modul_name="Station")
ABSAUGEN = GeraeteTestSchritt(name="Absaugen", modul_name="Station")
ZULAUF = GeraeteTestSchritt(name="Wasserzulauf", modul_name="Station")
ABPUMPEN = GeraeteTestSchritt(name="Wasser abpumpen", modul_name="Station")
HEISSWASSER = GeraeteTestSchritt(name="Heißwasserkreislauf", modul_name="Station")

# Standards
Funktionstest_Standard1 = [
    GEHT_AN, VERBINDET_SICH, LAEDT, FINDET_HEIM, SAUGT,
    STATION_GEHT_AN, SIGNAL, LAEDT_ROBOTER, REINIGUNG, ABSAUGEN
]

Funktionstest_Standard2 = [
    GEHT_AN, VERBINDET_SICH, LAEDT, FINDET_HEIM, SAUGT, WISCHT, GIBT_WASSER,
    STATION_GEHT_AN, SIGNAL, LAEDT_ROBOTER, REINIGUNG, ABSAUGEN, ZULAUF, ABPUMPEN
]

test_standards = {
    "Funktionstest-Standard1": Funktionstest_Standard1,
    "Funktionstest-Standard2": Funktionstest_Standard2
}

