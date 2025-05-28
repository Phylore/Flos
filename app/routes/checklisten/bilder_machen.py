# app/routes/checklisten/bilder_machen.py

from flask import Blueprint, request, redirect, url_for, render_template, flash
import os
from werkzeug.utils import secure_filename
from models.bild_db import GeraetBild
from models.geraet_db import Geraet
from database import db
from models.historie_db import Historie
from flask_login import current_user

def bilder_einpackfertig_pruefen(geraet_id):
    benoetigte_bilder = ["Produktansicht", "Unten", "Frontal", "Hinten"]
    return all(
        GeraetBild.query.filter_by(geraet_id=geraet_id, beschreibung=b).first()
        for b in benoetigte_bilder
    )

def bilder_fertig_pruefen(geraet_id):
    benoetigte_bilder = ["Produktansicht", "Unten", "Frontal", "Hinten", "Verpackt mit Etikett"]
    return all(
        GeraetBild.query.filter_by(geraet_id=geraet_id, beschreibung=b).first()
        for b in benoetigte_bilder
    )

bilder_bp = Blueprint("bildermachen", __name__, url_prefix="/checkliste/bilder")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bilder_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
def bilder_hochladen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    bilder = GeraetBild.query.filter_by(geraet_id=geraet.id).all()

    if request.method == "POST":
        feldname = request.form.get("feldname")  # z. B. "frontal"
        datei = request.files.get("bild")

        if not feldname or not datei:
            flash("❌ Ungültiger Upload. Feld oder Datei fehlt.", "danger")
            return redirect(request.url)

        beschreibung = feldname.replace("_", " ").capitalize()  # z. B. "Frontal"

        vorhandenes = GeraetBild.query.filter_by(geraet_id=geraet.id, beschreibung=beschreibung).first()

        filename = secure_filename(f"{geraet.qrcode}_{feldname}.jpg")
        pfad_fs = os.path.join(UPLOAD_FOLDER, filename)
        datei.save(pfad_fs)

        # Pfad nur relativ zu 'static/' speichern für URL
        pfad_db = f"uploads/{filename}"

        if vorhandenes:
            vorhandenes.pfad = pfad_db
            flash(f"♻️ Bild für „{beschreibung}“ ersetzt.", "info")
        else:
            neues_bild = GeraetBild(geraet_id=geraet.id, pfad=pfad_db, beschreibung=beschreibung)
            db.session.add(neues_bild)
            flash(f"✅ Bild für „{beschreibung}“ gespeichert.", "success")

        db.session.commit()

        # Flag: Bilder einpackfertig (4 Pflichtbilder) setzen oder zurücksetzen
        if bilder_einpackfertig_pruefen(geraet.id):
            geraet.bilder_einpackfertig = True
        else:
            geraet.bilder_einpackfertig = False

        # Flag: Bilder fertig (alle 5 Bilder) setzen oder zurücksetzen
        if bilder_fertig_pruefen(geraet.id):
            geraet.bilder_fertig = True
            eintrag = Historie(
                geraet_id=geraet.id,
                benutzer_id=current_user.id,
                aktion="Alle Bilder hochgeladen"
            )
            db.session.add(eintrag)
        else:
            geraet.bilder_fertig = False

        db.session.commit()

        return redirect(request.url)

    return render_template("checklisten/bildermachen.html", geraet=geraet, bilder=bilder)

