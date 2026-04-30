from fastapi import FastAPI #erstellt deine API
from fastapi.middleware.cors import CORSMiddleware #erlaubt Zugriff vom Frontend
from app.database import create_db #erstellt Tabellen
from app.routers import router #enthält alle API-Endpunkte
from app.seed_data import seed_data #fügt Testdaten ein

app = FastAPI(title="Workplace Booking App") #Initialisierung FastAPI-Anwendung

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://workplace-app-projekt.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #frontend und backend läuft separat, die Verbindung wird nicht blockiert

@app.on_event("startup")
def on_startup():
    create_db() #Tabellen Erstellung
    seed_data() #Einfügen Beispieldaten

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(router) #Router einbinden