# /app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import string
import requests
from bs4 import BeautifulSoup
from .schemas import ShortenedURLCreate, ShortenedURLResponse  # Import des schémas Pydantic
from .models import ShortenedURL

app = FastAPI()

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

# Configurer CORS pour permettre la communication entre frontend et backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend React (port 5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurer SQLAlchemy pour SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./db/mydatabase.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Exemple de modèle pour la table des URLs raccourcies
class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    title = Column(String)

# Créer les tables dans la base de données SQLite
Base.metadata.create_all(bind=engine)

# Fonction utilitaire pour générer un code court
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Route pour créer un URL raccourci
@app.post("/api/shorten/", response_model=ShortenedURLResponse)
async def shorten_url(request: ShortenedURLCreate):
    # Vérifier si l'URL existe déjà dans la base de données
    db = SessionLocal()
    existing_entry = db.query(ShortenedURL).filter(ShortenedURL.original_url == request.original_url).first()
    if existing_entry:
        return ShortenedURLResponse(id=existing_entry.id, short_code=existing_entry.short_code, 
                                    original_url=existing_entry.original_url, title=existing_entry.title)

    # Créer un nouveau code court
    short_code = generate_short_code()
    while db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first():
        short_code = generate_short_code()

    # Scraper le titre de la page originale
    try:
        response = requests.get(request.original_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
    except Exception:
        title = "No Title"

    # Sauvegarder l'URL raccourcie dans la base de données
    new_url = ShortenedURL(original_url=request.original_url, short_code=short_code, title=title)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return ShortenedURLResponse(id=new_url.id, short_code=new_url.short_code, original_url=new_url.original_url, title=new_url.title)

# Route pour obtenir la liste des URLs raccourcies
@app.get("/api/list/", response_model=list[ShortenedURLResponse])
async def list_short_urls():
    db = SessionLocal()
    shortlinks = db.query(ShortenedURL).order_by(ShortenedURL.id.desc()).all()
    return [ShortenedURLResponse(id=link.id, original_url=link.original_url, short_code=link.short_code, title=link.title) for link in shortlinks]

# Route pour obtenir l'URL originale à partir d'un short_code
@app.get("/api/urls/{short_code}", response_model=ShortenedURLResponse)
async def get_original_url(short_code: str):
    db = SessionLocal()
    entry = db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first()
    if entry:
        return ShortenedURLResponse(id=entry.id, short_code=entry.short_code, original_url=entry.original_url, title=entry.title)
    raise HTTPException(status_code=404, detail="Shortlink not found")

# Route pour rediriger vers l'URL originale à partir du short_code
@app.get("/go/{short_code}")
async def redirect_url(short_code: str):
    db = SessionLocal()
    entry = db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first()
    if entry:
        return RedirectResponse(url=entry.original_url)
    raise HTTPException(status_code=404, detail="Shortlink not found")

# Route d'accueil
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with SQLite!"}
