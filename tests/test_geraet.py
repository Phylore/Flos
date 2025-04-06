# tests/test_geraet.py
from geraete.geraet import Geraet

def test_dummy():
    g = Geraet("SN-001", None)
    assert g.seriennummer == "SN-001"

