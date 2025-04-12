from flask import Blueprint, render_template
from flask_login import login_required
from models.geraet_db import Geraet
from models.zustand_db import Zustand

auspacken_bp = Blueprint("auspacken", __name__, url_prefix="/checkliste/auspacken")

@auspacken_bp.route("/<int:geraet_id>")
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    zustaende = Zustand.query.all()
    return render_template("checklisten/auspacken.html", geraet=geraet, zustaende=zustaende)
