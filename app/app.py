from flask import Flask, render_template
from app.routes.geraete_routes import geraete_bp  # Importiere die richtigen Routen
from database import db  # Importiere db aus database.py

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///geraete.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisiere db
db.init_app(app)

# Registriere Blueprints
app.register_blueprint(geraete_bp, url_prefix='/geraete')
app.register_blueprint(geraete_bp)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

