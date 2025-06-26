# /app/routes/debug_test.py

from flask import Blueprint, jsonify
from app.models.geraet_db import Geraet
from app.models.teil_db import Teil
from app.models.zustand_db import Zustand
from database import db

debug_bp = Blueprint("debug", __name__)

@debug_bp.route("/debug/geraet/<int:geraet_id>")
def debug_geraet_teile(geraet_id):
    geraet = Geraet.query.get_or_404(geraet_id)
    teile = Teil.query.filter_by(geraet_id=geraet.id).all()
    zustaende = Zustand.query.all()

    data = {
        "geraet": {
            "id": geraet.id,
            "qrcode": geraet.qrcode,
            "modell": geraet.modell.name
        },
        "teile": [
            {
                "id": teil.id,
                "vorlage_name": getattr(teil.vorlage, "name", "??"),
                "zustand_id": teil.zustand_id
            }
            for teil in teile
        ],
        "zustaende": [ {"id": z.id, "name": z.name} for z in zustaende ]
    }

    return jsonify(data)
