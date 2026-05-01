import os #Umgebzungsvariablen zugreiffen
from pathlib import Path #Dateipfade bauen
from sqlmodel import SQLModel, create_engine #Verbindungsschicht zur Datenbank

db_path = os.getenv("DB_PATH") #Umgebungsvariable prüfen

if db_path:
    DATABASE_URL = f"sqlite:///{db_path}"
else:
    BASE_DIR = Path(__file__).resolve().parent.parent #Ordner backend
    DATABASE_PATH = BASE_DIR / "database.db" #Datenbank festlegen
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}" # aus dem Pfad die URL für SQLModel

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} #Arbeiten mit mehreren Zugriffe auf Datenbank
) #Verwaltung zur Datenbank


def create_db():
    SQLModel.metadata.create_all(engine) #alle Datenmodelle in die passenden Tabellen anlegen