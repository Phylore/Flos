# routes/geraet.py
from flask import Blueprint, render_template, redirect, url_for, request
from models import db, Geraet, Historie, Zustand  # Importiere deine Klassen

geraet_bp = Blueprint('geraet', __name__)

@geraet_bp.route('/geraet/<int:geraet_id>')
def geraet_detail(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    aktuelle_historie = Historie.query.filter_by(geraet_id=geraet.id).order_by(Historie.zeitpunkt.desc()).all()
    return render_template('geraet.html', geraet=geraet, historie=aktuelle_historie)

