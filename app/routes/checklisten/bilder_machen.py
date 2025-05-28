# app/routes/checklisten/bilder_machen.py

from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import os
from models.bild_db import GeraetBild
from models.geraet_db import Geraet
from database import db

bilder_bp = Blueprint("bildermachen", __name__, url_prefix="/checkliste/bilder")

UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bilder_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
def bilder_hochladen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    bildtypen = [
        ("produktansicht", "Produktansicht"),
        ("unten", "Unten"),
        ("frontal", "Frontal"),
        ("hinten", "Hinten"),
        ("verpackt_mit_etikett", "Verpackt mit Etikett"),
    ]

    if request.method == "POST":
        fehlend = False
        for feldname, beschreibung in bildtypen:
            file = request.files.get(feldname)
            if not file:
                flash(f"❌ Fehlendes Bild: {beschreibung}")
                fehlend = True
            else:
                filename = secure_filename(f"{geraet.qrcode}_{feldname}.jpg")
                pfad = os.path.join(UPLOAD_FOLDER, filename)
                file.save(pfad)
                db.session.add(GeraetBild(geraet_id=geraet.id, pfad=pfad, beschreibung=beschreibung))

        if fehlend:
            return redirect(request.url)

        db.session.commit()
        flash("✅ Alle Bilder erfolgreich gespeichert.")
        return redirect(url_for("geraete.bilder_hochladen", geraet_id=geraet.id))

    return render_template("checklisten/bildermachen.html", geraet=geraet)

