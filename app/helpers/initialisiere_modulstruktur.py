from models.modul_db import Modul
from models.teil_db import Teil
from models.zustand_db import Zustand
from database import db
from models.modelle.saugroboter_modelle import saugroboter_modelle
from models.modelle.stabstaubsauger_modelle import stabstaubsauger_modelle
from models.modul_defaults_db import module_standards

# Kombination aller bekannten Modelle
alle_modelldefinitionen = {
    **saugroboter_modelle,
    **stabstaubsauger_modelle
}

def get_default_zustand_id(kategorie, value):
    zustand = Zustand.query.filter_by(kategorie=kategorie, value=value).first()
    return zustand.id if zustand else None

def initialisiere_module_und_teile(geraet):
    modell_name = geraet.modell.name
    if modell_name not in alle_modelldefinitionen:
        print(f"❌ Kein Modul-Setup für Modell: {modell_name}")
        return

    modulstruktur = alle_modelldefinitionen[modell_name].get("module", {})

    anwesenheit_default = get_default_zustand_id("Anwesenheit", "Nicht geprüft")
    sauberkeit_default = get_default_zustand_id("Sauberkeit", "Nicht bewertet")

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
            db.session.flush()

            # Teile aus den Standardwerten anlegen
            for teilvorlage in module_standards[key]:
                teil = Teil(
                    name=teilvorlage.name,
                    modul_id=modul.id,
                    geraet_id=geraet.id,
                    teilvorlage_id=getattr(teilvorlage, "id", None),
                    anwesenheit_id=anwesenheit_default,
                    sauberkeit_id=sauberkeit_default
                )
                db.session.add(teil)

    db.session.commit()
    print(f"✅ Module & Teile für {modell_name} ({geraet.qrcode}) initialisiert.")

