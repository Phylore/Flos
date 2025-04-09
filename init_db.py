from app.app import app
from database import db
from models import *  # <-- registriert alle Tabellen sauber
from app.setup.setup_modelle_import import import_modelle_wenn_notwendig

with app.app_context():
    db.create_all()
    import_modelle_wenn_notwendig()

