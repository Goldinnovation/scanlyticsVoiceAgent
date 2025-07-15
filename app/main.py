from fastapi import APIRouter, FastAPI
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Oder z.B. ["http://localhost:5173"] für mehr Sicherheit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)