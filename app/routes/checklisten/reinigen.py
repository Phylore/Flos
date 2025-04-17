from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.zustand_db import Zustand
from models.teil_db import Teil
from models.historie_db import Historie
from database import db

reinigen_bp = Blueprint("reinigen", __name__, url_prefix="/checkliste/reinigen")

def ist_reinigung_vollständig(geraet):
    return all(
        teil.sauberkeit and teil.sauberkeit.value != "Nicht bewertet"
        for teil in geraet.teile
    )

@reinigen_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    sauberkeits_zustaende = Zustand.query.filter_by(kategorie="Sauberkeit").all()

    if request.method == "POST":
        saubere_teile = []
        veraendert = False

        for teil in geraet.teile:
            field_name = f"sauberkeit_{teil.id}"
            if field_name in request.form:
                neue_zustands_id = int(request.form[field_name])
                if teil.sauberkeit_id != neue_zustands_id:
                    teil.sauberkeit_id = neue_zustands_id
                    veraendert = True

                zustand = Zustand.query.get(neue_zustands_id)
                if zustand and zustand.value == "sauber":
                    saubere_teile.append(teil.name)

        if veraendert:
            db.session.commit()

            if ist_reinigung_vollständig(geraet):
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

