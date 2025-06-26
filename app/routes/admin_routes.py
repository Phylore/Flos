# admin_routes.py
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from app.models.lieferant_db import Lieferant  # Passe ggf. deinen Pfad an
from database import db
from flask_login import login_required, current_user
from app.models.geraet_db import Geraet as GeraetDB

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
    # Dummy-Ansicht – später mit echten Daten füllen
    chargen = []
    return render_template('chargenansicht.html', chargen=chargen)

@admin_bp.route("/charge_anlegen", methods=["GET", "POST"])
@login_required
def charge_anlegen():
    if not current_user.ist_admin:
        abort(403)
    from app.models.geraet_db import Geraet as GeraetDB
    geraete = GeraetDB.query.all()
    if request.method == "POST":
        # Hier später: neue Charge speichern!
        # Formulardaten auswerten...
        return redirect(url_for('admin.chargen'))
    return render_template("chargen_neu.html", geraete=geraete)


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
            # Existiert der Name schon?
            exists = Lieferant.query.filter_by(name=name).first()
            if exists:
                flash("Ein Lieferant mit diesem Namen existiert bereits.", "warning")
            else:
                lieferant = Lieferant(name=name)
                db.session.add(lieferant)
                db.session.commit()
                flash(f"Lieferant '{name}' wurde angelegt.", "success")
                return redirect(url_for("admin.charge_anlegen"))
    return render_template("lieferant_neu.html")


