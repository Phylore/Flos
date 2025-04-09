from app import app, db
from models.benutzer_db import Benutzer

with app.app_context():
    # Admin anlegen
    admin = Benutzer.query.filter_by(name="admin").first()
    if not admin:
        admin = Benutzer(name="admin")
        admin.set_passwort("admin")  # Passwort setzen (wird gehasht)
        db.session.add(admin)

    # Eric anlegen
    eric = Benutzer.query.filter_by(name="eric").first()
    if not eric:
        eric = Benutzer(name="eric")
        eric.set_passwort("eric")  # Passwort setzen (wird gehasht)
        db.session.add(eric)

    db.session.commit()

    print("✅ Admin und Eric wurden erfolgreich hinzugefügt.")

