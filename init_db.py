# init_db.py
from app.app import app
from database import db
from models.geraet_db import Geraet
from models.kategorie_db import Kategorie
from models.modul_db import Modul
from models.modell_db import Modell
from models.benutzer_db import Benutzer
from models.historie_db import Historie
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig

with app.app_context():
    db.create_all()
    import_modelle_wenn_notwendig()

