# app/app.py

from flask import Flask
from app.routes.geraete_routes import geraete_bp

app = Flask(__name__)
app.register_blueprint(geraete_bp)

