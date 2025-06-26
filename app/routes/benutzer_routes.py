from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.geraet_db import Geraet as GeraetDB
from app.models.benutzer_db import Benutzer

benutzer_bp = Blueprint("benutzer", __name__)  # Das MUSS am Anfang stehen!

@benutzer_bp.route("/benutzer/mein_konto", methods=["GET", "POST"])
@login_required
def mein_konto():
    if request.method == "POST":
        neues_passwort = request.form.get("neues_passwort")
        if neues_passwort:
            current_user.passwort = generate_password_hash(neues_passwort)
            from database import db
            db.session.commit()
            flash("Passwort erfolgreich geändert.", "success")
            return redirect(url_for("benutzer.mein_konto"))
        else:
            flash("Bitte ein neues Passwort eingeben.", "warning")
    return render_template("mein_konto.html", benutzer=current_user)

@benutzer_bp.route("/benutzer/dashboard")
@login_required
def dashboard():
    geraete = (
        GeraetDB.query
        .filter_by(benutzer_id=current_user.id)
        .order_by(GeraetDB.id.desc())  # sortiert nach zuletzt erstelltem Gerät
        .all()
    )
    return render_template("dashboard.html", geraete=geraete)

@benutzer_bp.route("/benutzer/passwort_aendern", methods=["GET", "POST"])
@login_required
def passwort_aendern():
    if request.method == "POST":
        neues_passwort = request.form.get("neues_passwort")
        passwort_bestaetigen = request.form.get("passwort_bestaetigen")
        if not neues_passwort:
            flash("Bitte ein neues Passwort eingeben.", "warning")
        elif neues_passwort != passwort_bestaetigen:
            flash("Die Passwörter stimmen nicht überein.", "danger")
        else:
            current_user.set_passwort(neues_passwort)
            from database import db
            db.session.commit()
            flash("Passwort erfolgreich geändert.", "success")
            return redirect(url_for("benutzer.mein_konto"))
    return render_template("passwort_aendern.html")



