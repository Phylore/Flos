from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, abort
from flask_login import current_user, login_required
from models.kategorie_db import Kategorie
from models.modell_db import Modell
from models.geraet_db import Geraet as GeraetDB
from models.hersteller_db import Hersteller
from models.zustand_db import Zustand
from models.historie_db import Historie
from models.teil_db import Teil, TeilVorlage
from app.helpers.initialisiere_modulstruktur import initialisiere_module_und_teile
from app.helpers.initialisiere_teststruktur import initialisiere_tests_fuer_geraet
from app.helpers.initialisiere_testdurchlauf import initialisiere_testdurchlauf


from database import db

geraete_bp = Blueprint("geraete", __name__, url_prefix="/geraete")


@geraete_bp.route("/scannen", methods=["GET", "POST"])
@login_required
def scannen():
    if request.method == "POST":
        qrcode = request.form["code"]
        geraet_db = GeraetDB.query.filter_by(qrcode=qrcode).first()
        if geraet_db:
            return redirect(url_for('geraete.geraet_seite', qrcode=geraet_db.qrcode))
        else:
            kategorien = Kategorie.query.all()
            hersteller = Hersteller.query.all()
            return render_template("geraet_neu.html", kategorien=kategorien, modelle=[], hersteller=hersteller, qr_code=qrcode)
    return render_template("scannen.html")


@geraete_bp.route("/geraet/neu", methods=["GET"])
@login_required
def geraet_neu():
    qr_code = request.args.get("qr_code")
    kategorien = Kategorie.query.all()
    modelle = Modell.query.all()
    hersteller = Hersteller.query.all()
    return render_template("geraet_neu.html", kategorien=kategorien, modelle=modelle, hersteller=hersteller, qr_code=qr_code)


@geraete_bp.route("/geraet", methods=["POST"])
@login_required
def geraet_anlegen():
    qrcode = request.form["qrcode"]
    modell_id = request.form["modell"]

    existing = GeraetDB.query.filter_by(qrcode=qrcode).first()
    if existing:
        return redirect(url_for("geraete.geraet_seite", qrcode=existing.qrcode))

    zustand = Zustand.query.filter_by(value="Ja", kategorie="Funktioniert").first()

    neues_geraet = GeraetDB(
        qrcode=qrcode,
        modell_id=modell_id,
        zustand_id=zustand.id,
        benutzer_id=current_user.id
    )
    db.session.add(neues_geraet)
    db.session.commit()

    initialisiere_module_und_teile(neues_geraet)
    initialisiere_tests_fuer_geraet(neues_geraet)
    initialisiere_testdurchlauf(neues_geraet)

    eintrag = Historie(
        geraet_id=neues_geraet.id,
        benutzer_id=current_user.id,
        aktion="Gerät angelegt"
    )
    db.session.add(eintrag)
    db.session.commit()

    return redirect(url_for("geraete.geraet_seite", qrcode=neues_geraet.qrcode))


@geraete_bp.route("/geraet/<qrcode>", endpoint="geraet_seite")
@login_required
def geraet_seite(qrcode):
    geraet = GeraetDB.query.filter_by(qrcode=qrcode).first_or_404()
    return render_template("geraet.html", geraet=geraet)


@geraete_bp.route("/modelle/<int:kategorie_id>")
@login_required
def modelle_fuer_kategorie(kategorie_id):
    modelle = Modell.query.filter_by(kategorie_id=kategorie_id).all()
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])


@geraete_bp.route("/geraet/<string:qrcode>/historie")
@login_required
def geraet_historie(qrcode):
    geraet = GeraetDB.query.filter_by(qrcode=qrcode).first_or_404()
    historie_eintraege = Historie.query.filter_by(geraet_id=geraet.id).order_by(Historie.zeitpunkt.desc()).all()
    return render_template("historie.html", geraet=geraet, historie=historie_eintraege)


@geraete_bp.route("/geraet/<string:qrcode>/loeschen", methods=["POST"])
@login_required
def geraet_loeschen(qrcode):
    geraet = GeraetDB.query.filter_by(qrcode=qrcode).first_or_404()

    von_user = db.session.query(Historie).filter_by(
        geraet_id=geraet.id,
        benutzer_id=current_user.id
    ).first()

    if not von_user:
        flash("Du darfst dieses Gerät nicht löschen.", "danger")
        return redirect(url_for("benutzer.dashboard"))

    Historie.query.filter_by(geraet_id=geraet.id).delete()
    db.session.delete(geraet)

    try:
        db.session.commit()
        flash("Gerät wurde gelöscht.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"Fehler beim Löschen: {str(e)}", "danger")

    return redirect(url_for("benutzer.dashboard"))


# 🔄 Neue API-Endpunkte für dynamische Dropdowns

@geraete_bp.route("/api/kategorien")
@login_required
def api_kategorien():
    hersteller_id = request.args.get("hersteller_id", type=int)
    kategorien = Kategorie.query.join(Modell).filter(Modell.hersteller_id == hersteller_id).distinct()
    return jsonify([{"id": k.id, "name": k.name} for k in kategorien])


@geraete_bp.route("/api/modelle")
@login_required
def api_modelle():
    hersteller_id = request.args.get("hersteller_id", type=int)
    kategorie_id = request.args.get("kategorie_id", type=int)
    modelle = Modell.query.filter_by(hersteller_id=hersteller_id, kategorie_id=kategorie_id).all()
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])

@geraete_bp.route("/api/unterkategorien")
@login_required
def api_unterkategorien():
    kategorie_id = request.args.get("kategorie_id", type=int)
    if not kategorie_id:
        return jsonify([])

    unterkats = Unterkategorie.query.filter_by(kategorie_id=kategorie_id).all()
    return jsonify([{"id": u.id, "name": u.name} for u in unterkats])
