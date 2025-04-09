from flask import render_template
from flask_login import login_required, current_user
from models.geraet_db import Geraet as GeraetDB
from flask import Blueprint

benutzer_bp = Blueprint("benutzer", __name__)

@benutzer_bp.route("/benutzer/dashboard")
@login_required
def dashboard():
    geraete = (
        GeraetDB.query
        .filter_by(benutzer_id=current_user.id)
        .order_by(GeraetDB.id.desc())  # sortiert nach zuletzt erstelltem Gerät
        .all()
    )
    return render_template("dashboard.html", geraete=geraete)

