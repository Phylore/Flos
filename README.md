# Flos – Geräteverwaltungssystem

Dies ist ein modulares Gerätetracker-System auf Basis von Python, Flask und SQLAlchemy.

## Features

- Objektorientiertes Modell: Geräte → Modelle → Kategorien → Module → Teile
- Web-Oberfläche mit Flask
- Zustandsverwaltung mit Historie
- Datenbankstruktur mit SQLite + SQLAlchemy
- Unit-Tests mit pytest

## Setup

```bash
git clone https://github.com/Phylore/Flos.git
cd Flos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. FLASK_APP=app/app.py flask run

