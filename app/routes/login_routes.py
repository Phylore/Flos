# /app/routes/login_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.benutzer_db import Benutzer
from database import db

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        passwort = request.form["passwort"]

        benutzer = db.session.query(Benutzer).filter_by(name=name).first()

        if benutzer and benutzer.check_passwort(passwort):
            login_user(benutzer)  # ✅ Login via Flask-Login
            flash("Login erfolgreich.")
            # NEU: Admin-Weiterleitung!
            if benutzer.ist_admin:
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("benutzer.dashboard"))
        else:
            flash("Login fehlgeschlagen.")
    return render_template("login.html")

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()  # ✅ Logout via Flask-Login
    flash("Erfolgreich ausgeloggt.")
    return redirect(url_for("login.login"))

