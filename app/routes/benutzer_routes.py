from flask import Blueprint, render_template, session
from models.benutzer_db import Benutzer
from models.geraet_db import Geraet

benutzer_bp = Blueprint("benutzer", __name__)

@benutzer_bp.route("/benutzer/dashboard")
def dashboard():
    benutzer_id = session.get("benutzer_id")
    if not benutzer_id:
        return "Nicht eingeloggt", 401

    geraete = []  # später kommen hier die Benutzergeräte rein
    return render_template("dashboard.html", geraete=geraete)

