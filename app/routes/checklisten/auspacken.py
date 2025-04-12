from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.zustand_db import Zustand
from models.teil_db import Teil
from database import db

auspacken_bp = Blueprint("auspacken", __name__, url_prefix="/checkliste/auspacken")

@auspacken_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    anwesenheits_zustaende = Zustand.query.filter_by(kategorie="Anwesenheit").all()

    if request.method == "POST":
        for teil in geraet.teile:
            field_name = f"anwesenheit_{teil.id}"
            if field_name in request.form:
                neue_zustands_id = int(request.form[field_name])
                teil.anwesenheit_id = neue_zustands_id
        db.session.commit()
        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/auspacken.html", geraet=geraet, zustaende=anwesenheits_zustaende)
