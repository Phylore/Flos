# /app/routes/geraete_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_required
from models.kategorie_db import Kategorie
from models.modell_db import Modell
from models.geraet_db import Geraet as GeraetDB
from models.zustand_db import Zustand
from models.historie_db import Historie
from models.teil_db import TeilVorlage  # notwendig für GET /auspacken
from app.helpers.initialisiere_teile import initialisiere_teile_fuer_geraet
from database import db



geraete_bp = Blueprint("geraete", __name__)


@geraete_bp.route("/scannen", methods=["GET", "POST"])
@login_required
def scannen():
    if request.method == "POST":
        qrcode = request.form["code"]
        geraet_db = db.session.query(GeraetDB).filter_by(qrcode=qrcode).first()

        if geraet_db:
            return redirect(url_for('geraete.geraet_seite', qrcode=geraet_db.qrcode))

        else:
            kategorien = Kategorie.query.all()
            return render_template("geraet_neu.html", kategorien=kategorien, modelle=[], qr_code=qrcode)

    return render_template("scannen.html")


@geraete_bp.route("/geraet", methods=["POST"])
@login_required
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
        zustand_id=1,
        benutzer_id=current_user.id
    )
    db.session.add(neues_geraet)
    db.session.commit()

    # 🧩 Teile initialisieren
    initialisiere_teile_fuer_geraet(neues_geraet)

    return redirect(url_for("geraete.geraet_seite", qrcode=neues_geraet.qrcode))


@geraete_bp.route("/modelle/<int:kategorie_id>")
@login_required
def modelle_fuer_kategorie(kategorie_id):
    modelle = Modell.query.filter_by(kategorie_id=kategorie_id).all()
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])


@geraete_bp.route("/geraet/<int:geraet_id>/auspacken", methods=["GET"])
@login_required
def auspacken_popup(geraet_id):
    geraet = db.session.query(GeraetDB).get_or_404(geraet_id)
    zustaende = Zustand.query.all()
    teile = db.session.query(Teil).filter_by(geraet_id=geraet.id).all()

    return render_template("auspacken.html", geraet=geraet, zustaende=zustaende, teile=teile)

@geraete_bp.route("/geraet/<string:qrcode>")
@login_required
def geraet_seite(qrcode):
    geraet = db.session.query(GeraetDB).filter_by(qrcode=qrcode).first_or_404()
    return render_template("geraet.html", geraet=geraet)


@geraete_bp.route("/geraet/<int:geraet_id>/zustand", methods=["POST"])
@login_required
def zustand_aendern(geraet_id):
    geraet = db.session.query(GeraetDB).get_or_404(geraet_id)
    neuer_zustand_id = int(request.form["zustand_id"])

    if geraet.zustand_id != neuer_zustand_id:
        geraet.zustand_id = neuer_zustand_id
        eintrag = Historie(
            geraet_id=geraet.id,
            aktion=f"Zustand geändert zu '{Zustand.query.get(neuer_zustand_id).name}'",
            benutzer_id=current_user.id
        )
        db.session.add(eintrag)
        db.session.commit()

    return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))


@geraete_bp.route("/anzeigen", methods=["POST"])
@login_required
def geraet_anzeigen():
    qrcode = request.form.get("qrcode")
    if not qrcode:
        flash("Kein Gerät ausgewählt.")
        return redirect(url_for("benutzer.dashboard"))
    return redirect(url_for("geraete.geraet_seite", qrcode=qrcode))
