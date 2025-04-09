from flask import Flask
from database import db  # <--- WICHTIG: deine echte Instanz
from app.app import app

# Imports aus dem Projekt
from models.teil_db import Teil
from models.modul_db import Modul

with app.app_context():
    db.create_all()
    print("🧪 Mapped models:")
    print(db.Model.metadata.tables.keys())

