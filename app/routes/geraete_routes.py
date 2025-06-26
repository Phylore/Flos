from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, abort, session
from flask_login import current_user, login_required
from app.models.kategorie_db import Kategorie, Unterkategorie
from app.models.modell_db import Modell
from app.models.geraet_db import Geraet as GeraetDB
from app.models.hersteller_db import Hersteller
from app.models.zustand_db import Zustand
from app.models.historie_db import Historie
from app.models.teil_db import Teil, TeilVorlage
from app.helpers.initialisiere_modulstruktur import initialisiere_module_und_teile
from app.helpers.initialisiere_teststruktur import initialisiere_tests_fuer_geraet
from app.helpers.initialisiere_testdurchlauf import initialisiere_testdurchlauf
from database import db
from rapidfuzz import process  # fuzzy match

geraete_bp = Blueprint("geraete", __name__, url_prefix="/geraete")

# --- 1. Geräteeingabe/Anlage/Detail ---

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
    modell_id = request.form.get("modell")
    neues_modell_name = request.form.get("neues_modell", "").strip()
    aktion = request.form.get("aktion")

    if modell_id:
        modell = Modell.query.get(int(modell_id))
    elif neues_modell_name:
        alle_modellnamen = [m.name for m in Modell.query.all()]
        match = process.extractOne(neues_modell_name, alle_modellnamen)
        if match:
            vorschlag, score = match[0], match[1]
        else:
            vorschlag, score = None, 0

        if score > 85:
            flash(f"Meintest du: {vorschlag}? Falls ja, wähle es bitte im Dropdown.", "warning")
            return redirect(url_for("geraete.geraet_neu", qr_code=qrcode))
        else:
            flash(f"Modell '{neues_modell_name}' wird neu angelegt.", "info")
            return redirect(url_for("geraete.modell_neu_wizard", modellname=neues_modell_name, qrcode=qrcode))
    else:
        flash("Bitte Modell wählen oder neues Modell eingeben.", "danger")
        return redirect(url_for("geraete.geraet_neu", qr_code=qrcode))

    if GeraetDB.query.filter_by(qrcode=qrcode).first():
        return redirect(url_for("geraete.geraet_seite", qrcode=qrcode))

    zustand = Zustand.query.filter_by(value="Ja", kategorie="Funktioniert").first()

    neues_geraet = GeraetDB(
        qrcode=qrcode,
        modell_id=modell.id,
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


@geraete_bp.route("/geraet/<qrcode>")
@login_required
def geraet_seite(qrcode):
    geraet = GeraetDB.query.filter_by(qrcode=qrcode).first_or_404()
    return render_template("geraet.html", geraet=geraet)

# --- 2. Modell-Wizard ---

@geraete_bp.route("/modell/neu", methods=["GET"])
@login_required
def modell_neu_wizard():
    modellname = request.args.get("modellname")
    qrcode = request.args.get("qrcode")
    hersteller = Hersteller.query.all()
    kategorien = Kategorie.query.all()
    return render_template("modell_neu.html", modellname=modellname, qrcode=qrcode, hersteller=hersteller, kategorien=kategorien)

@geraete_bp.route("/modell/speichern", methods=["POST"])
@login_required
def modell_speichern():
    name = request.form["modellname"].strip()
    qrcode = request.form.get("qrcode")
    
    # Hersteller: Auswahl oder Neuanlage
    hersteller_id = request.form.get("hersteller_id")
    neuer_hersteller = request.form.get("neuer_hersteller", "").strip()
    if hersteller_id == "__neu__" and neuer_hersteller:
        h = Hersteller.query.filter_by(name=neuer_hersteller).first()
        if not h:
            h = Hersteller(name=neuer_hersteller)
            db.session.add(h)
            db.session.commit()
        hersteller_id = h.id

    # Kategorie: Auswahl oder Neuanlage
    kategorie_id = request.form.get("kategorie_id")
    neue_kategorie = request.form.get("neue_kategorie", "").strip()
    if kategorie_id == "__neu__" and neue_kategorie:
        k = Kategorie.query.filter_by(name=neue_kategorie).first()
        if not k:
            k = Kategorie(name=neue_kategorie)
            db.session.add(k)
            db.session.commit()
        kategorie_id = k.id

    # Unterkategorie: Auswahl oder Neuanlage (unique per Kategorie)
    unterkategorie_id = request.form.get("unterkategorie_id")
    neue_unterkategorie = request.form.get("neue_unterkategorie", "").strip()
    if unterkategorie_id == "__neu__" and neue_unterkategorie and kategorie_id:
        uk = Unterkategorie.query.filter_by(name=neue_unterkategorie, kategorie_id=kategorie_id).first()
        if not uk:
            uk = Unterkategorie(name=neue_unterkategorie, kategorie_id=kategorie_id)
            db.session.add(uk)
            db.session.commit()
        unterkategorie_id = uk.id

    # Doppelte Modellnamen verhindern
    exists = Modell.query.filter_by(name=name).first()
    if exists:
        flash("Modellname existiert bereits. Bitte anderen Namen wählen.", "danger")
        return redirect(url_for("geraete.modell_neu_wizard", modellname=name, qrcode=qrcode))

    neues_modell = Modell(
        name=name,
        hersteller_id=hersteller_id,
        kategorie_id=kategorie_id,
        unterkategorie_id=unterkategorie_id or None
    )
    db.session.add(neues_modell)
    db.session.commit()

    flash("Neues Modell wurde gespeichert.", "success")
    return redirect(url_for("geraete.geraet_neu", qr_code=qrcode))

   


# --- 3. Historie und Löschen ---

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

# --- 4. API und Hilfsrouten ---

@geraete_bp.route("/api/kategorien")
@login_required
def api_kategorien():
    hersteller_id = request.args.get("hersteller_id")
    kategorien = (
        Kategorie.query
        .join(Modell)
        .filter(Modell.hersteller_id == hersteller_id)
        .distinct()
        .all()
    )
    return jsonify([{"id": k.id, "name": k.name} for k in kategorien])

@geraete_bp.route("/api/unterkategorien")
@login_required
def api_unterkategorien():
    kategorie_id = request.args.get("kategorie_id")
    unterkategorien = (
        Unterkategorie.query
        .filter_by(kategorie_id=kategorie_id)
        .all()
    )
    return jsonify([{"id": u.id, "name": u.name} for u in unterkategorien])

@geraete_bp.route("/api/modelle")
@login_required
def api_modelle():
    hersteller_id = request.args.get("hersteller_id")
    kategorie_id = request.args.get("kategorie_id")
    unterkategorie_id = request.args.get("unterkategorie_id")
    modelle = (
        Modell.query
        .filter_by(hersteller_id=hersteller_id, kategorie_id=kategorie_id, unterkategorie_id=unterkategorie_id)
        .all()
    )
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])

@geraete_bp.route("/modelle/<int:kategorie_id>")
@login_required
def modelle_fuer_kategorie(kategorie_id):
    modelle = Modell.query.filter_by(kategorie_id=kategorie_id).all()
    return jsonify([{"id": m.id, "name": m.name} for m in modelle])

@geraete_bp.route("/api/unterkategorie_fuer_modell/<modellname>")
def get_unterkategorie_fuer_modell(modellname):
    modell = Modell.query.filter_by(name=modellname).first()
    if modell and modell.unterkategorie:
        return jsonify({"unterkategorie": modell.unterkategorie.name})
    return jsonify({"unterkategorie": None})

# --- 5. QR/Scan und Session ---

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

@geraete_bp.route("/aktives_geraet", methods=["POST"])
def set_aktives_geraet():
    data = request.get_json()
    session["aktives_geraet_id"] = data["geraet_id"]
    return "", 204


@geraete_bp.route("/api/aehnliche_modelle")
@login_required
def api_aehnliche_modelle():
    query = request.args.get("name", "").strip()
    if not query:
        return jsonify([])

    alle_modelle = Modell.query.all()
    alle_namen = [m.name for m in alle_modelle]
    matches = process.extract(query, alle_namen, limit=10)
    # Optional: Nur Treffer ab Score X anzeigen
    result = [{"name": name, "score": int(score)} for name, score, idx in matches if score > 60]
    return jsonify(result)

@geraete_bp.route("/modell/module", methods=["POST"])
@login_required
def modell_module():
    # Alle Formulardaten aus Schritt 1 übernehmen
    modellname = request.form.get("modellname", "")
    qrcode = request.form.get("qrcode", "")
    hersteller_id = request.form.get("hersteller_id", "")
    neuer_hersteller = request.form.get("neuer_hersteller", "")
    kategorie_id = request.form.get("kategorie_id", "")
    neue_kategorie = request.form.get("neue_kategorie", "")
    unterkategorie_id = request.form.get("unterkategorie_id", "")
    neue_unterkategorie = request.form.get("neue_unterkategorie", "")

    # Optional: Du kannst auch alles an ein dict packen und ans Template übergeben
    return render_template(
        "modell_module.html",
        modellname=modellname,
        qrcode=qrcode,
        hersteller_id=hersteller_id,
        neuer_hersteller=neuer_hersteller,
        kategorie_id=kategorie_id,
        neue_kategorie=neue_kategorie,
        unterkategorie_id=unterkategorie_id,
        neue_unterkategorie=neue_unterkategorie,
        bekannte_module=[],  # später ersetzen!
    )

