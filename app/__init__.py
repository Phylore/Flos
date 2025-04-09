from .app import app
from database import db
from flask_migrate import Migrate  # Flask-Migrate hinzufügen

migrate = Migrate(app, db)  # Migration initialisieren

