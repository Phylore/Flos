from geraete.modelle import DreameL10
from geraete.geraet import Geraet
from geraete.zustand import Zustand

modell = DreameL10()
g = Geraet("SR-2024-001", modell)

print(g)
g.aktualisiere_zustand(Zustand.EINGELAGERT)
print(g.zeige_historie())

