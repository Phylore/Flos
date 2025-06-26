# Datei: app/routes/checklisten/funktionstest.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.geraet_db import Geraet
from app.models.geraetetest_db import GeraeteTestSchritt, GeraeteTestDurchlauf, GeraeteTestErgebnis
from app.models.historie_db import Historie
from database import db

funktionstest_bp = Blueprint("funktionstest", __name__, url_prefix="/checkliste/funktionstest")

@funktionstest_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)

    gruppiert = {}
    for schritt in GeraeteTestSchritt.query.order_by(GeraeteTestSchritt.id).all():
        gruppe = schritt.modul_name or "Gerät"
        gruppiert.setdefault(gruppe, []).append(schritt)

    letzter = GeraeteTestDurchlauf.query.filter_by(geraet_id=geraet.id)\
        .order_by(GeraeteTestDurchlauf.zeitpunkt.desc()).first()

    bestandene_ids = set()
    nichtbestandene_ids = set()
    if letzter:
        bestandene_ids = {
            e.schritt_id for e in GeraeteTestErgebnis.query
            .filter_by(durchlauf_id=letzter.id, bestanden=True).all()
        }
        nichtbestandene_ids = {
            e.schritt_id for e in GeraeteTestErgebnis.query
            .filter_by(durchlauf_id=letzter.id, bestanden=False).all()
        }

    if request.method == "POST":
        neue_ergebnisse = {}
        for key, val in request.form.items():
            if key.startswith("schritt_"):
                schritt_id = int(key.split("_")[1])
                if val in ["ja", "nein"]:
                    neue_ergebnisse[schritt_id] = (val == "ja")

        bestandene_ids_neu = {sid for sid, bestanden in neue_ergebnisse.items() if bestanden}
        veraendert = bestandene_ids_neu != bestandene_ids

        if veraendert:
            durchlauf = GeraeteTestDurchlauf(geraet_id=geraet.id, benutzer_id=current_user.id)
            db.session.add(durchlauf)
            db.session.flush()

            kommentar_liste = []
            alle_ids = [s.id for gruppe in gruppiert.values() for s in gruppe]

            for gruppe in gruppiert.values():
                for schritt in gruppe:
                    if schritt.id in neue_ergebnisse:
                        bestanden = neue_ergebnisse[schritt.id]
                        if bestanden:
                            kommentar_liste.append(schritt.name)

                        db.session.add(GeraeteTestErgebnis(
                            durchlauf_id=durchlauf.id,
                            schritt_id=schritt.id,
                            bestanden=bestanden
                        ))

            if set(alle_ids) == bestandene_ids_neu:
                kommentar = f"Bestanden: {', '.join(kommentar_liste)}" if kommentar_liste else None
                db.session.add(Historie(
                    geraet_id=geraet.id,
                    benutzer_id=current_user.id,
                    aktion="Funktionstest durchgeführt",
                    kommentar=kommentar
                ))
                # Gerät-Flag setzen!
                geraet.getestet = True  # <- Attribut ggf. anpassen!
            db.session.commit()

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/funktionstest.html",
                           geraet=geraet,
                           gruppiert=gruppiert,
                           bestandene_ids=bestandene_ids,
                           nichtbestandene_ids=nichtbestandene_ids)

