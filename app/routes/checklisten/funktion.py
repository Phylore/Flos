from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.historie_db import Historie
from database import db

funktion_bp = Blueprint("funktion", __name__, url_prefix="/checkliste/funktion")

# 👇 Tests gruppiert nach Modul
FUNKTIONSTESTS = {
    "Roboter": {
        "geht_an": "Gerät geht an",
        "verbindet_sich": "Verbindet sich",
        "laedt": "Lädt",
        "findet_heim": "Findet heim",
        "saugt": "Saugt",
        "wischt": "Wischt",
        "gibt_wasser": "Gibt Wasser"
    },
    "Station": {
        "station_geht_an": "Station geht an",
        "signal": "Gibt Signal",
        "laedt_roboter": "Lädt Roboter",
        "zulauf": "Wasserzulauf",
        "abpumpen": "Wasser abpumpen",
        "reinigung": "Selbstreinigung"
    }
}

@funktion_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)

    if request.method == "POST":
        ausgewaehlt = request.form.getlist("tests")
        bestandene = []

        for gruppe, tests in FUNKTIONSTESTS.items():
            for key, beschreibung in tests.items():
                if key in ausgewaehlt:
                    bestandene.append(f"{gruppe}: {beschreibung}")

        kommentar = "Bestanden: " + ", ".join(bestandene) if bestandene else None

        if bestandene:
            eintrag = Historie(
                geraet_id=geraet.id,
                benutzer_id=current_user.id,
                aktion="Funktionstest durchgeführt",
                kommentar=kommentar
            )
            db.session.add(eintrag)
            db.session.commit()

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/funktion.html", geraet=geraet, tests=FUNKTIONSTESTS)

