# init_db.py
from app.app import app
from database import db
from models.geraet_db import Geraet
from models.modell_db import Modell
from models.benutzer_db import Benutzer
from models.historie_db import Historie

with app.app_context():
    db.create_all()

    # Beispielnutzer anlegen (nur wenn er noch nicht existiert)
    if not Benutzer.query.filter_by(name="admin").first():
        benutzer = Benutzer(name="admin")
        benutzer.set_passwort("passwort123")
        db.session.add(benutzer)
        db.session.commit()
        print("Beispielnutzer 'admin' wurde angelegt.")
    else:
        print("Benutzer 'admin' existiert bereits.")
