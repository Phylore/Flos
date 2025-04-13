from app.app import app
from database import db
from sqlalchemy import text

with app.app_context():
    db.session.execute(text("DROP TABLE IF EXISTS _alembic_tmp_geraete"))
    db.session.commit()
    print("✅ Temporäre Tabelle _alembic_tmp_geraete wurde gelöscht.")