

from flask_migrate import Migrate
from flask import Flask, render_template
from .routes.geraete_routes import geraete_bp
from .routes.login_routes import login_bp
from .routes.benutzer_routes import benutzer_bp
from .routes.admin_routes import admin_bp
from .routes.debug_test import debug_bp
from .routes.checklisten.auspacken import auspacken_bp
from .routes.checklisten.reinigen import reinigen_bp
from .routes.checklisten.funktionstest import funktionstest_bp
from .routes.checklisten.einpacken import einpacken_bp
from .routes.checklisten.bilder_machen import bilder_bp

from database import db
from app.models.geraet_db import Geraet
from app.models.charge_db import Charge
from app.models.lieferant_db import Lieferant
import os

app = Flask(__name__, static_folder="../static")


# Absoluter Pfad zur Datenbankdatei
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "../geraete.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey")

# Initialisiere db
db.init_app(app)

#Migriere DB
migrate = Migrate(app,db)
# Initialisiere LoginManager
from flask_login import LoginManager
from app.models.benutzer_db import Benutzer

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
app.register_blueprint(admin_bp)
app.register_blueprint(debug_bp)  # ✅ Jetzt an richtiger Stelle
app.register_blueprint(auspacken_bp)
app.register_blueprint(reinigen_bp)
app.register_blueprint(funktionstest_bp)
app.register_blueprint(einpacken_bp)
app.register_blueprint(bilder_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

