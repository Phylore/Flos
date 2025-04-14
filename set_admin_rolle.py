from app.app import app
from database import db
from models.benutzer_db import Benutzer

with app.app_context():
    admin = Benutzer.query.filter_by(name='admin').first()
    if admin:
        admin.rolle = 'admin'
        db.session.commit()
        print("✅ Benutzer 'admin' hat jetzt die Rolle 'admin'.")
    else:
        print("❌ Benutzer 'admin' nicht gefunden!")