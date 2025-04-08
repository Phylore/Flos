from flask import request, render_template, redirect, url_for, session, flash
from models.benutzer_db import Benutzer
from database import db

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        passwort = request.form["passwort"]
        benutzer = db.session.query(Benutzer).filter_by(name=name).first()

        if benutzer and benutzer.check_passwort(passwort):
            session["benutzer_id"] = benutzer.id
            flash("Login erfolgreich.")
            return redirect(url_for("geraete.scannen"))  # oder Dashboard
        else:
            flash("Login fehlgeschlagen.")
    return render_template("login.html")

