from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.geraet_db import Geraet
from models.historie_db import Historie
from models.teil_db import Teil
from models.modul_db import Modul
from database import db
from models.ersatzteil_defaults_db import ersatzteil_set_namen, lade_vorlagen
from models.modelle.saugroboter_modelle import saugroboter_modelle

einpacken_bp = Blueprint("einpacken", __name__, url_prefix="/checkliste/einpacken")

def ist_auspacken_abgeschlossen(geraet):
    return all(
        teil.anwesenheit and teil.anwesenheit.value != "Nicht geprüft"
        for teil in geraet.teile
        if teil.anwesenheit_id is not None
    )

def ist_reinigung_abgeschlossen(geraet):
    return all(
        teil.sauberkeit and teil.sauberkeit.value != "Nicht geprüft"
        for teil in geraet.teile
        if teil.sauberkeit_id is not None
    )

# TODO: Funktionstest-Abgeschlossenheitsprüfung kannst du später nach gleichem Schema bauen
def ist_funktion_abgeschlossen(geraet_id):
    return db.session.query(Historie).filter_by(
        geraet_id=geraet_id,
        aktion="Funktionstest durchgeführt"
    ).count() > 0

@einpacken_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)

    # ECHTE Checkstatus der vorherigen Listen
    status = {
        "auspacken": ist_auspacken_abgeschlossen(geraet),
        "reinigung": ist_reinigung_abgeschlossen(geraet),
        "funktion": ist_funktion_abgeschlossen(geraet.id)
    }

    modell_info = saugroboter_modelle.get(geraet.modell.name, {})
    ersatz_options = modell_info.get("ersatzpakete", [])

    if request.method == "POST":
        ausgewaehlt = request.form.get("ersatzpaket")
        if not ausgewaehlt:
            flash("Bitte ein Ersatzteilpaket auswählen.", "warning")
            return redirect(request.url)

        namen_liste = ersatzteil_set_namen.get(ausgewaehlt, [])
        teilvorlagen = lade_vorlagen(namen_liste)

        # Neues Modul 'Ersatzteile' erstellen
        modul = Modul(name="Ersatzteile", geraet_id=geraet.id)
        db.session.add(modul)
        db.session.flush()

        for vorlage in teilvorlagen:
            if vorlage:
                teil = Teil(
                    name=vorlage.name,
                    geraet_id=geraet.id,
                    modul_id=modul.id,
                    teilvorlage_id=vorlage.id
                )
                db.session.add(teil)

        kommentar = f"Ersatzteilpaket '{ausgewaehlt}' verpackt"

        eintrag = Historie(
            geraet_id=geraet.id,
            benutzer_id=current_user.id,
            aktion="Gerät eingepackt",
            kommentar=kommentar
        )
        db.session.add(eintrag)
        db.session.commit()

        flash("Gerät wurde erfolgreich eingepackt.", "success")
        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template("checklisten/einpacken.html",
                           geraet=geraet,
                           status=status,
                           ersatzpakete=ersatz_options)

