from app.models.teil_db import Teil
from app.models.modul_db import Modul
from database import db
from app.models.zustand_db import Zustand
# Import für alle_teilvorlagen ggf. nur, falls du sie wirklich brauchst
# from app.helpers.saugroboter_teile import alle_teilvorlagen

def initialisiere_module_und_teile(geraet):
    # Defaults für Anwesenheit und Sauberkeit
    anwesenheit_default = 1
    sauberkeit_default = 1

    # Beispielhafter Import – passe ggf. den Pfad an dein Projekt an!
    from app.models.modelle.saugroboter.saugroboter_modul_defaults_db import module_standards

    for key in module_standards:
        modul = Modul(
            name=key,
            geraet_id=geraet.id
        )
        db.session.add(modul)
        db.session.commit()  # Modul braucht ID für FK unten

        for teilvorlage in module_standards[key]:
            # --- TEMPORÄRER FIX: Strings ODER Objekte zulassen (TODO!) ---
            # Nach Projekt refactoren: Nur noch TeilVorlage-Objekte verwenden!
            name = teilvorlage.name if hasattr(teilvorlage, "name") else str(teilvorlage)
            teil = Teil(
                name=name,
                modul_id=modul.id,
                geraet_id=geraet.id,
                teilvorlage_id=getattr(teilvorlage, "id", None),
                anwesenheit_id=anwesenheit_default,
                sauberkeit_id=sauberkeit_default
            )
            db.session.add(teil)
            # Debug-Print kannst du für Analyse rein-/rausnehmen:
            # print("DEBUG: Teilvorlage:", teilvorlage, "Type:", type(teilvorlage))

    db.session.commit()

