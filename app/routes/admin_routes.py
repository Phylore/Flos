# admin_routes.py

from flask import Blueprint, render_template, abort, request
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

