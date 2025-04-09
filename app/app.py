from flask import Flask, render_template
from app.routes.geraete_routes import geraete_bp  # Importiere die richtigen Routen
from app.routes.login_routes import login_bp
from app.routes.benutzer_routes import benutzer_bp
from database import db  # Importiere db aus database.py
import os


app = Flask(__name__)

# Absoluter Pfad zur Datenbankdatei
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "../geraete.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey")

# Initialisiere db
db.init_app(app)

# Initialisiere db
db.init_app(app)

# Initialisiere LoginManager
from flask_login import LoginManager
from models.benutzer_db import Benutzer

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"

@login_manager.user_loader
def load_user(user_id):
    return Benutzer.query.get(int(user_id))

# Registriere Blueprints
app.register_blueprint(geraete_bp, url_prefix='/geraete')
app.register_blueprint(login_bp)
app.register_blueprint(benutzer_bp)


# Registriere Blueprints
app.register_blueprint(geraete_bp, url_prefix='/geraete')
app.register_blueprint(login_bp)
app.register_blueprint(benutzer_bp)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

