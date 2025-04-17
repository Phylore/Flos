# Datei: app/routes/checklisten/funktionstest.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.geraetetest_db import GeraeteTestSchritt, GeraeteTestDurchlauf, GeraeteTestErgebnis
from models.historie_db import Historie
from database import db

funktionstest_bp = Blueprint("funktionstest", __name__, url_prefix="/checkliste/funktionstest")

@funktionstest_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)

    # Schritt-Liste nach Modul gruppieren
    gruppiert = {}
    for schritt in GeraeteTestSchritt.query.order_by(GeraeteTestSchritt.id).all():
        gruppe = schritt.modul_name or "Gerät"
        gruppiert.setdefault(gruppe, []).append(schritt)

    # Letzter Durchlauf
    letzter = GeraeteTestDurchlauf.query.filter_by(geraet_id=geraet.id)\
        .order_by(GeraeteTestDurchlauf.zeitpunkt.desc()).first()

    bestandene_ids = set()
    if letzter:
        bestandene_ids = {
            e.schritt_id for e in GeraeteTestErgebnis.query.filter_by(durchlauf_id=letzter.id, bestanden=True).all()
        }

    if request.method == "POST":
        neue_ids = set(int(i) for i in request.form.getlist("schritt"))
        veraendert = neue_ids != bestandene_ids

        if veraendert:
            durchlauf = GeraeteTestDurchlauf(geraet_id=geraet.id, benutzer_id=current_user.id)
            db.session.add(durchlauf)
            db.session.flush()

            kommentar_liste = []

            for gruppe in gruppiert.values():
                for schritt in gruppe:
                    bestanden = schritt.id in neue_ids
                    if bestanden:
                        kommentar_liste.append(schritt.name)

                    db.session.add(GeraeteTestErgebnis(
                        durchlauf_id=durchlauf.id,
                        schritt_id=schritt.id,
                        bestanden=bestanden
                    ))

            kommentar = f"Bestanden: {', '.join(kommentar_liste)}" if kommentar_liste else None
            db.session.add(Historie(
                geraet_id=geraet.id,
                benutzer_id=current_user.id,
                aktion="Funktionstest durchgeführt",
                kommentar=kommentar
            ))

            db.session.commit()

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/funktionstest.html",
                           geraet=geraet,
                           gruppiert=gruppiert,
                           bestandene_ids=bestandene_ids)

