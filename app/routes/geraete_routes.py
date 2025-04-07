from flask import Blueprint, render_template, request, redirect, url_for
from models.modell_db import Modell  # Achte darauf, dass du das Modell importierst
from models.geraet_db import Geraet as GeraetDB
from database import db

geraete_bp = Blueprint("geraete", __name__)

@geraete_bp.route("/scannen", methods=["GET", "POST"])
def scannen():
    if request.method == "POST":
        seriennummer = request.form["seriennummer"]
        geraet_db = db.session.query(GeraetDB).filter(GeraetDB.seriennummer == seriennummer).first()

        if geraet_db:
            return redirect(url_for('geraete.zeige_geraet', id=geraet_db.id))
        else:
            modelle = db.session.query(Modell).all()
            return render_template("geraet_neu.html", modelle=modelle)
    
    return render_template("scannen.html")

