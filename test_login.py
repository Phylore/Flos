# test_login.py
from app.app import app
from database import db
from models.benutzer_db import Benutzer
from werkzeug.security import check_password_hash

def login_test(benutzername: str, passwort: str):
    with app.app_context():
        user = Benutzer.query.filter_by(name=benutzername).first()
        if not user:
            print(f"❌ Benutzer '{benutzername}' nicht gefunden.")
            return
        if check_password_hash(user.passwort_hash, passwort):
            print(f"✅ Login für '{benutzername}' erfolgreich!")
        else:
            print(f"❌ Passwort für '{benutzername}' ist falsch.")

# 👉 Hier Testbenutzer eintragen
login_test("admin", "admin")
login_test("eric", "eric")
login_test("max", "max")  # Optional

