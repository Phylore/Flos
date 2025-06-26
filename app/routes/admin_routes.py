# admin_routes.py
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from app.models.lieferant_db import Lieferant  # Passe ggf. deinen Pfad an
from database import db
from flask_login import login_required, current_user
from app.models.geraet_db import Geraet as GeraetDB
from app.models.charge_db import Charge

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not current_user.ist_admin:
        abort(403)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    geraete = GeraetDB.query.order_by(GeraetDB.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("admin_dashboard.html", geraete=geraete)


@admin_bp.route('/admin/chargen')
@login_required
def chargen():
    chargen = Charge.query.order_by(Charge.id.desc()).all()
    return render_template('chargenansicht.html', chargen=chargen)



@admin_bp.route("/charge_anlegen", methods=["GET", "POST"])
@login_required
def charge_anlegen():
    if not current_user.ist_admin:
        abort(403)

    from app.models.geraet_db import Geraet as GeraetDB
    from app.models.lieferant_db import Lieferant

    geraete = GeraetDB.query.all()
    lieferanten = Lieferant.query.order_by(Lieferant.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        lieferant_id = request.form.get("lieferant_id")

        if not name or not lieferant_id:
            flash("Bitte alle Felder ausfüllen!", "danger")
            return render_template(
                "chargen_neu.html",
                geraete=geraete,
                lieferanten=lieferanten
            )

        neue_charge = Charge(
            name=name,
            lieferant_id=lieferant_id
        )
        db.session.add(neue_charge)
        db.session.commit()

        flash("Charge wurde erfolgreich gespeichert.", "success")
        return redirect(url_for('admin.chargen'))

    return render_template(
        "chargen_neu.html",
        geraete=geraete,
        lieferanten=lieferanten
    )




@admin_bp.route("/lieferant_anlegen", methods=["GET", "POST"])
@login_required
def lieferant_anlegen():
    if not current_user.ist_admin:
        abort(403)

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            flash("Bitte gib einen Namen für den Lieferanten an.", "danger")
        else:
            # Prüfen, ob der Lieferant bereits existiert
            if Lieferant.query.filter_by(name=name).first():
                flash("Ein Lieferant mit diesem Namen existiert bereits.", "warning")
            else:
                neuer_lieferant = Lieferant(name=name)
                db.session.add(neuer_lieferant)
                db.session.commit()
                flash(f"Lieferant '{name}' wurde erfolgreich angelegt.", "success")

                # Nach erfolgreichem Anlegen zurück zu 'Charger anlegen'
                return redirect(url_for("admin.charge_anlegen"))

    return render_template("lieferant_neu.html")



