# app/routes/geraete_routes.py

from flask import Blueprint, render_template
from geraete.modelle import DreameL10
from geraete.geraet import Geraet

geraete_bp = Blueprint("geraete", __name__)

geraet = Geraet("SR-0001", DreameL10())

@geraete_bp.route("/geraet")
def zeige_geraet():
    return render_template("geraet.html", geraet=geraet)

