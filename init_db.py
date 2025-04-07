# init_db.py
from app.app import app
from database import db
from models.modell_db import Modell

with app.app_context():
    db.create_all()

