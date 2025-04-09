from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Alle Modelle importieren
from models.teil_db import Teil
from models.modul_db import Modul

# Einmal das Mapping erzwingen
print("🧪 Mapped models:")
print(db.Model.metadata.tables.keys())

