from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app.models.geraet_db import Geraet
from app.models.zustand_db import Zustand
from app.models.teil_db import Teil
from database import db

zustand_aendern_bp = Blueprint("zustand_aendern", __name__, url_prefix="/checkliste/zustand_aendern")

@zustand_aendern_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    zustaende = Zustand.query.all()

    if request.method == "POST":
        for teil in geraet.teile:
            field_name = f"anwesenheit_{teil.id}"
            if field_name in request.form:
                teil.anwesenheit_id = int(request.form[field_name])
            field_name = f"sauberkeit_{teil.id}"
            if field_name in request.form:
                teil.sauberkeit_id = int(request.form[field_name])
            field_name = f"beschaedigung_{teil.id}"
            if field_name in request.form:
                teil.beschaedigung_id = int(request.form[field_name])
        db.session.commit()
        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/zustand_aendern.html", geraet=geraet, zustaende=zustaende)
