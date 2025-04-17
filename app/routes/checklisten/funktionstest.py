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
    schritte = GeraeteTestSchritt.query.order_by(GeraeteTestSchritt.id).all()

    # Letzter Durchlauf
    letzter = GeraeteTestDurchlauf.query.filter_by(geraet_id=geraet.id)\
        .order_by(GeraeteTestDurchlauf.zeitpunkt.desc()).first()

    bestandene_ids = set()
    if letzter:
        bestandene_ids = {
            e.schritt_id for e in GeraeteTestErgebnis.query.filter_by(durchlauf_id=letzter.id, bestanden=True).all()
        }

    if request.method == "POST":
        print("📥 Funktionstest POST erhalten")
        neue_ids = set(int(i) for i in request.form.getlist("schritt"))
        veraendert = neue_ids != bestandene_ids

        print(f"🧪 Alt: {bestandene_ids} / Neu: {neue_ids} / verändert? {veraendert}")

        if veraendert:
            durchlauf = GeraeteTestDurchlauf(geraet_id=geraet.id, benutzer_id=current_user.id)
            db.session.add(durchlauf)
            db.session.flush()

            kommentar_liste = []

            for schritt in schritte:
                bestanden = schritt.id in neue_ids
                if bestanden:
                    kommentar_liste.append(schritt.name)

                db.session.add(GeraeteTestErgebnis(
                    durchlauf_id=durchlauf.id,
                    schritt_id=schritt.id,
                    bestanden=bestanden
                ))

            kommentar = f"Bestanden: {', '.join(kommentar_liste)}" if kommentar_liste else None
            eintrag = Historie(
                geraet_id=geraet.id,
                benutzer_id=current_user.id,
                aktion="Funktionstest durchgeführt",
                kommentar=kommentar
            )
            db.session.add(eintrag)
            db.session.commit()
            print("💾 Funktionstest gespeichert")
        else:
            print("⚠️ Keine Änderungen – kein Commit")

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/funktionstest.html", geraet=geraet, schritte=schritte, bestandene_ids=bestandene_ids)

