from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db
from app.routers import router
from app.seed_data import seed_data

app = FastAPI(title="Workplace Booking App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://workplace-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db()
    seed_data()

app.include_router(router)