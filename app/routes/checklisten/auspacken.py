from flask import Blueprint, render_template
from models.geraet_db import Geraet

auspacken_bp = Blueprint("auspacken", __name__, url_prefix="/checkliste/auspacken")

@auspacken_bp.route("/<int:geraet_id>")
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    return render_template("checklisten/auspacken.html", geraet=geraet)

