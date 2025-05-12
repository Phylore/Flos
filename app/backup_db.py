import os
import sqlite3
import shutil

def backup_database():
    # Absoluter Pfad zur SQLite-Datenbank
    db_path = "/home/amt/Schreibtisch/QRC/geraete.db"
    
    # Zielordner für das Backup
    backup_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Zielpfad für das Backup
    backup_path = os.path.join(backup_dir, "geraete_backup.db")

    # Kopiere die Originaldatenbank in das Backup-Verzeichnis
    shutil.copy(db_path, backup_path)
    
    print(f"Backup erfolgreich: {backup_path}")
    return backup_path

if __name__ == "__main__":
    backup_database()

