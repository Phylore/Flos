# init_db.py

from database import Base, engine
from models.modell_db import Modell

# Hier später auch andere Tabellen importieren (z. B. Geraet)

Base.metadata.create_all(bind=engine)
print("Tabellen wurden erstellt.")

