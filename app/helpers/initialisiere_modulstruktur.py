from models.modul_db import Modul
from models.teil_db import Teil
from database import db
from app.setup.saugroboter_modelle import saugroboter_modelle
from app.setup.modul_defaults_db import module_standards

def initialisiere_module_und_teile(geraet):
    modell_name = geraet.modell.name
    if modell_name not in saugroboter_modelle:
        print(f"❌ Kein Modul-Setup für Modell: {modell_name}")
        return

    modell_config = saugroboter_modelle[modell_name]
    modulstruktur = modell_config.get("module", {})

    for modul_bezeichnung, default_key in modulstruktur.items():
        if isinstance(default_key, list):
            default_keys = default_key
        else:
            default_keys = [default_key]

        for key in default_keys:
            if key not in module_standards:
                print(f"⚠️ Kein Modul-Standard definiert für: {key}")
                continue

            modul = Modul(
                name=modul_bezeichnung,
                geraet_id=geraet.id
            )
            db.session.add(modul)
            db.session.flush()  # sorgt für modul.id

            for teilvorlage in module_standards[key]:
                teil = Teil(
                    name=teilvorlage.name,
                    modul_id=modul.id,
                    teilvorlage_id=teilvorlage.id  # falls du das nutzt
                )
                db.session.add(teil)

    db.session.commit()
    print(f"✅ Module und Teile für {modell_name} ({geraet.qrcode}) initialisiert.")

