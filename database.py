# database.py
from flask_sqlalchemy import SQLAlchemy

# Initialisiere SQLAlchemy
db = SQLAlchemy()

# Definiere Base, das die Grundlage für alle Modelle bildet
Base = db.Model

