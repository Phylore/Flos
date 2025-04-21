from models.hersteller_db import Hersteller
from database import db

def init_hersteller():
    hersteller_namen = [
        "iRobot", "Ecovacs", "Dreame", "Eureka", "Samsung", "Hanseatic"
    ]

    for name in hersteller_namen:
        if not Hersteller.query.filter_by(name=name).first():
            db.session.add(Hersteller(name=name))

    db.session.commit()
    print("✅ Hersteller eingefügt.")

