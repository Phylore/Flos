from app.app import app
from database import db
from models.geraet_db import Geraet
from models.benutzer_db import Benutzer

with app.app_context():
    admin = Benutzer.query.filter_by(name='admin').first()
    if not admin:
        raise Exception("⚠️ Kein Benutzer mit Name 'admin' gefunden!")

    updated = 0
    for geraet in Geraet.query.filter_by(benutzer_id=None).all():
        geraet.benutzer_id = admin.id
        updated += 1

    db.session.commit()
    print(f"✅ {updated} Geräte dem Benutzer 'admin' zugewiesen.")