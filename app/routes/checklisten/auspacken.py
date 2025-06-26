from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.geraet_db import Geraet
from app.models.zustand_db import Zustand
from app.models.teil_db import Teil
from app.models.historie_db import Historie
from database import db

auspacken_bp = Blueprint("auspacken", __name__, url_prefix="/checkliste/auspacken")

def alle_teile_abgehakt(geraet):
    return all(
        teil.anwesenheit and teil.anwesenheit.value in ["Ja", "Ersetzt"]
        for teil in geraet.teile
    )

@auspacken_bp.route("/<int:geraet_id>", methods=["GET", "POST"])
@login_required
def anzeigen(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    anwesenheits_zustaende = Zustand.query.filter_by(kategorie="Anwesenheit").all()

    if request.method == "POST":
        print("📥 POST erhalten – Verarbeitung beginnt")
        anwesende_teile = []
        veraendert = False

        for teil in geraet.teile:
            field_name = f"anwesenheit_{teil.id}"
            if field_name in request.form:
                neue_zustands_id = int(request.form[field_name])
                alt_id = teil.anwesenheit_id
                print(f"🔄 {teil.name}: alt={alt_id}, neu={neue_zustands_id}")

                if alt_id != neue_zustands_id:
                    teil.anwesenheit_id = neue_zustands_id
                    veraendert = True
                    print(f"✅ {teil.name} geändert")

                zustand = Zustand.query.get(neue_zustands_id)
                if zustand and zustand.value == "Ja":
                    anwesende_teile.append(teil.name)

        if veraendert:
            print("💾 Änderungen erkannt → Speichern")
            db.session.commit()

            if alle_teile_abgehakt(geraet):
                kommentar = f"Anwesend: {', '.join(anwesende_teile)}" if anwesende_teile else None
                eintrag = Historie(
                    geraet_id=geraet.id,
                    benutzer_id=current_user.id,
                    aktion="Auspacken abgeschlossen",
                    kommentar=kommentar
                )
                db.session.add(eintrag)

                # **NEU**: Geraet-Flag direkt setzen!
                geraet.ausgepackt = True  # <- Attributname ggf. anpassen!
                db.session.commit()
                print("🟢 Auspacken abgeschlossen gespeichert")
            else:
                print("🟡 Noch nicht alle Teile korrekt markiert – kein Historieneintrag")
        else:
            print("⚠️ Keine Änderungen erkannt – kein Commit")

        return redirect(url_for("geraete.geraet_seite", qrcode=geraet.qrcode))

    print("📄 GET: Lade Geräteseite")
    for teil in geraet.teile:
        print(f"📦 {teil.name} – anwesenheit_id={teil.anwesenheit_id}")

    # **Nur noch das Geraet-Objekt, KEIN Status-Dict!**
    return render_template("checklisten/auspacken.html", geraet=geraet, zustaende=anwesenheits_zustaende)

