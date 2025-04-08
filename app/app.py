from flask import Flask, render_template
from app.routes.geraete_routes import geraete_bp  # Importiere die richtigen Routen
from database import db  # Importiere db aus database.py
import os
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey")


app = Flask(__name__)

# Absoluter Pfad zur Datenbankdatei
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "../geraete.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisiere db
db.init_app(app)

# Registriere Blueprints
app.register_blueprint(geraete_bp, url_prefix='/geraete')


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

