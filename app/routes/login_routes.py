# login_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
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
            session["benutzer_id"] = benutzer.id
            session["benutzer_name"] = benutzer.name
            flash("Login erfolgreich.")
            return redirect(url_for("geraete.scannen"))
        else:
            flash("Login fehlgeschlagen.")
    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("benutzer_id", None)
    session.pop("benutzer_name", None)
    flash("Du wurdest ausgeloggt.")
    return redirect(url_for("index"))

