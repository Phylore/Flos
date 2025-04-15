from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.zustand_db import Zustand
from models.historie_db import Historie
from database import db

reinigen_bp = Blueprint("reinigen", __name__, url_prefix="/checkliste/reinigen")

@reinigen_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    sauberkeits_zustaende = Zustand.query.filter_by(kategorie="Sauberkeit").all()

    if request.method == "POST":
        saubere_teile = []

        for teil in geraet.teile:
            field_name = f"sauberkeit_{teil.id}"
            if field_name in request.form:
                neue_id = int(request.form[field_name])
                teil.sauberkeit_id = neue_id
                if teil.sauberkeit and teil.sauberkeit.value == "sauber":
                    saubere_teile.append(teil.name)

        db.session.commit()

        kommentar = f"Sauber: {', '.join(saubere_teile)}" if saubere_teile else None
        eintrag = Historie(
            geraet_id=geraet.id,
            benutzer_id=current_user.id,
            aktion="Reinigung durchgeführt",
            kommentar=kommentar
        )
        db.session.add(eintrag)
        db.session.commit()

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/reinigen.html", geraet=geraet, zustaende=sauberkeits_zustaende)

