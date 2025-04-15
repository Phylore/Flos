from models.modul_db import Modul
from models.teil_db import Teil
from database import db
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modul_defaults_db import module_standards
from models.teilvorlage_db import TeilVorlage  # Import der TeilVorlage

def initialisiere_module_und_teile(geraet):
    modell_name = geraet.modell.name
    if modell_name not in saugroboter_modelle:
        print(f"❌ Kein Modul-Setup für Modell: {modell_name}")
        return

    modulstruktur = saugroboter_modelle[modell_name].get("module", {})

    for modul_bezeichnung, standard_keys in modulstruktur.items():
        if isinstance(standard_keys, list):
            default_keys = standard_keys
        else:
            default_keys = [standard_keys]

        for key in default_keys:
            if key not in module_standards:
                print(f"⚠️ Kein Modul-Standard definiert für: {key}")
                continue

            # Modul in der Datenbank erstellen
            modul = Modul(name=modul_bezeichnung, geraet_id=geraet.id)
            db.session.add(modul)
            db.session.flush()  # damit modul.id existiert

            # Teile aus den Standardwerten anlegen
            for teilvorlage in module_standards[key]:
                # Stelle sicher, dass `TeilVorlage` korrekt zugewiesen wird
                teilvorlage_obj = TeilVorlage.query.filter_by(name=teilvorlage).first()

                teil = Teil(
                    name=teilvorlage,
                    modul_id=modul.id,
                    teilvorlage_id=teilvorlage_obj.id if teilvorlage_obj else None
                )
                db.session.add(teil)

    db.session.commit()
    print(f"✅ Module & Teile für {modell_name} ({geraet.qrcode}) initialisiert.")

