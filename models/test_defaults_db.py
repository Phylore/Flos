from models.geraetetest_db import GeraeteTestSchritt

# Roboter-Schritte
GEHT_AN = GeraeteTestSchritt(name="Gerät geht an")
VERBINDET_SICH = GeraeteTestSchritt(name="Verbindet sich")
LAEDT = GeraeteTestSchritt(name="Lädt")
FINDET_HEIM = GeraeteTestSchritt(name="Findet heim")
SAUGT = GeraeteTestSchritt(name="Saugt")
WISCHT = GeraeteTestSchritt(name="Wischt")
GIBT_WASSER = GeraeteTestSchritt(name="Gibt Wasser")

# Station-Schritte
STATION_GEHT_AN = GeraeteTestSchritt(name="Station geht an")
SIGNAL = GeraeteTestSchritt(name="Gibt Signal")
LAEDT_ROBOTER = GeraeteTestSchritt(name="Lädt Roboter")
REINIGUNG = GeraeteTestSchritt(name="Selbstreinigung")
ABSAUGEN = GeraeteTestSchritt(name="Absaugen")
ZULAUF = GeraeteTestSchritt(name="Wasserzulauf")
ABPUMPEN = GeraeteTestSchritt(name="Wasser abpumpen")
HEISSWASSER = GeraeteTestSchritt(name="Heißwasserkreislauf")

# Standards
Funktionstest_Standard1 = [
    # Roboter
    GEHT_AN, VERBINDET_SICH, LAEDT, FINDET_HEIM, SAUGT,
    # Station
    STATION_GEHT_AN, SIGNAL, LAEDT_ROBOTER, REINIGUNG, ABSAUGEN
]

Funktionstest_Standard2 = [
    # Roboter
    GEHT_AN, VERBINDET_SICH, LAEDT, FINDET_HEIM, SAUGT, WISCHT, GIBT_WASSER,
    # Station
    STATION_GEHT_AN, SIGNAL, LAEDT_ROBOTER, REINIGUNG, ABSAUGEN, ZULAUF, ABPUMPEN
]

test_standards = {
    "Funktionstest-Standard1": Funktionstest_Standard1,
    "Funktionstest-Standard2": Funktionstest_Standard2
}

