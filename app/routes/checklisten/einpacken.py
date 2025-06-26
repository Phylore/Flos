from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.geraet_db import Geraet
from app.models.historie_db import Historie
from app.models.teil_db import Teil
from app.models.modul_db import Modul
from app.models.geraetetest_db import GeraeteTestSchritt, GeraeteTestDurchlauf, GeraeteTestErgebnis
from database import db
from app.models.ersatzteil_defaults_db import ersatzteil_set_namen, lade_vorlagen
from app.models.modelle.saugroboter_modelle import saugroboter_modelle
import json

einpacken_bp = Blueprint("einpacken", __name__, url_prefix="/checkliste/einpacken")

def ist_auspacken_abgeschlossen(geraet):
    return all(
        teil.anwesenheit and teil.anwesenheit.value in ["Ja", "Ersetzt"]
        for teil in geraet.teile
    )

def ist_reinigung_abgeschlossen(geraet):
    return all(
        teil.sauberkeit and teil.sauberkeit.value != "Nicht bewertet"
        for teil in geraet.teile
    )

def ist_funktion_abgeschlossen(geraet_id):
    letzter = GeraeteTestDurchlauf.query.filter_by(geraet_id=geraet_id)\
        .order_by(GeraeteTestDurchlauf.zeitpunkt.desc()).first()
    if not letzter:
        return False

    alle_schritte = GeraeteTestSchritt.query.count()
    bestandene = GeraeteTestErgebnis.query.filter_by(durchlauf_id=letzter.id, bestanden=True).count()
    return bestandene >= alle_schritte

@einpacken_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)

    # Status-Checks als boolsche Flags:
    auspacken_status = ist_auspacken_abgeschlossen(geraet)
    reinigung_status = ist_reinigung_abgeschlossen(geraet)
    funktion_status = ist_funktion_abgeschlossen(geraet.id)
    bilder_status = getattr(geraet, "bilder_einpackfertig", False)

    # Flags im Gerät setzen, falls abweichend
    changed = False
    if geraet.ausgepackt != auspacken_status:
        geraet.ausgepackt = auspacken_status
        changed = True
    if geraet.gereinigt != reinigung_status:
        geraet.gereinigt = reinigung_status
        changed = True
    if getattr(geraet, "getestet", None) != funktion_status:
        setattr(geraet, "getestet", funktion_status)
        changed = True

    if changed:
        db.session.commit()

    # Ersatzteilpakete holen wie gehabt
    modell_info = saugroboter_modelle.get(geraet.modell.name, {})
    ersatz_options = modell_info.get("ersatzteilpakete", [])

    # Paket-Teile für dynamische Anzeige im Frontend
    ersatz_inhalt_dict = {
        name: ersatzteil_set_namen.get(name, [])
        for name in ersatz_options
    }

    if request.method == "POST":
        # Check: Alles erledigt?
        if not (geraet.ausgepackt and geraet.gereinigt and geraet.getestet and bilder_status):
            flash("Nicht alle Prüfungen abgeschlossen – Einpacken nicht möglich.", "danger")
            return redirect(request.url)

        ausgewaehlt = request.form.get("ersatzpaket")
        if not ausgewaehlt:
            flash("Bitte ein Ersatzteilpaket auswählen.", "warning")
            return redirect(request.url)

        namen_liste = ersatzteil_set_namen.get(ausgewaehlt, [])
        teilvorlagen = lade_vorlagen(namen_liste)

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

        # Kommentar zum Paket
        kommentar = f"Ersatzteilpaket '{ausgewaehlt}' verpackt"
        eintrag = Historie(
            geraet_id=geraet.id,
            benutzer_id=current_user.id,
            aktion="Gerät eingepackt",
            kommentar=kommentar
        )
        db.session.add(eintrag)

        # Optional: Du kannst jetzt ein neues Geräteflag „eingepackt“ setzen, falls du möchtest:
        # geraet.eingepackt = True

        db.session.commit()

        flash("Gerät wurde erfolgreich eingepackt.", "success")
        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    return render_template(
        "checklisten/einpacken.html",
        geraet=geraet,
        ersatzpakete=ersatz_options,
        ersatzpaket_inhalt_json=json.dumps(ersatz_inhalt_dict)
    )

