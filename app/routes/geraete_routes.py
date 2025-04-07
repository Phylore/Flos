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

