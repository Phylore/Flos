# /app/routes/geraete_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from models.kategorie_db import Kategorie
from models.modell_db import Modell
from models.geraet_db import Geraet as GeraetDB
from models.zustand_db import Zustand
from models.historie_db import Historie
from database import db

geraete_bp = Blueprint("geraete", __name__)


@geraete_bp.route("/scannen", methods=["GET", "POST"])
def scannen():
    if request.method == "POST":
        qrcode = request.form["code"]
        geraet_db = db.session.query(GeraetDB).filter_by(qrcode=qrcode).first()

        if geraet_db:
            return redirect(url_for('geraete.zeige_geraet', id=geraet_db.id))
        else:
            kategorien = Kategorie.query.all()
            return render_template("geraet_neu.html", kategorien=kategorien, modelle=[], qr_code=qrcode)

    return render_template("scannen.html")


@geraete_bp.route("/geraet", methods=["POST"])
def geraet_anlegen():
    qrcode = request.form["qrcode"]
    modell_id = request.form["modell"]

    # ✅ Gerät existiert schon → weiterleiten statt Error
    existing = GeraetDB.query.filter_by(qrcode=qrcode).first()
    if existing:
        return redirect(url_for("geraete.geraet_seite", qrcode=existing.qrcode))

    # ❗ Neues Gerät anlegen
    neues_geraet = GeraetDB(
        qrcode=qrcode,
        modell_id=modell_id,
        zustand_id=1
    )
    neues_geraet.benutzer_id = current_user.id
    db.session.add(neues_geraet)
    db.session.commit()

    return redirect(url_for("geraete.geraet_seite", qrcode=neues_geraet.qrcode))



@geraete_bp.route("/modelle/<int:kategorie_id>")
def modelle_fuer_kategorie(kategorie_id):
    modelle = Modell.query.filter_by(kategorie_id=kategorie_id).all()
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])


@geraete_bp.route("/geraet/<int:geraet_id>/auspacken", methods=["GET", "POST"])
def auspacken(geraet_id):
    geraet = db.session.query(GeraetDB).get_or_404(geraet_id)
    zustaende = db.session.query(Zustand).all()

    if request.method == "POST":
        for modul in geraet.modell.module:
            for teil in modul.teile:
                form_key = f"teil_{teil.id}"
                if form_key in request.form:
                    neuer_zustand_id = int(request.form[form_key])
                    if teil.zustand_id != neuer_zustand_id:
                        teil.zustand_id = neuer_zustand_id
                        eintrag = Historie(
                            geraet_id=geraet.id,
                            text=f"Teil '{teil.name}' in Modul '{modul.name}' geändert zu '{Zustand.query.get(neuer_zustand_id).value}'"
                        )
                        db.session.add(eintrag)

        db.session.commit()
        return redirect(url_for("geraete.zeige_geraet", id=geraet.id))

    return render_template("auspacken.html", geraet=geraet, zustaende=zustaende)

@geraete_bp.route("/geraet/<string:qrcode>")
def geraet_seite(qrcode):
    geraet = db.session.query(GeraetDB).filter_by(qrcode=qrcode).first_or_404()
    return render_template("geraet.html", geraet=geraet)

@geraete_bp.route("/geraet/<int:geraet_id>/zustand", methods=["POST"])
def zustand_aendern(geraet_id):
    geraet = db.session.query(GeraetDB).get_or_404(geraet_id)
    neuer_zustand_id = int(request.form["zustand_id"])

    # Nur ändern, wenn es tatsächlich ein anderer ist
    if geraet.zustand_id != neuer_zustand_id:
        geraet.zustand_id = neuer_zustand_id

        # Historieneintrag (optional)
        eintrag = Historie(
            geraet_id=geraet.id,
            aktion=f"Zustand geändert zu '{Zustand.query.get(neuer_zustand_id).name}'",
            benutzer_id=1  # ❗ Später dynamisch mit aktuellem User
        )
        db.session.add(eintrag)

    db.session.commit()
    return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))


