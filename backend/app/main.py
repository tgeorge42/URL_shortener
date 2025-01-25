# /app/main.py
from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import string
import requests
from bs4 import BeautifulSoup
from .schemas import ShortenedURLCreate, ShortenedURLResponse
from .models import ShortenedURL
import os

# Fonction pour obtenir l'engine avec l'URL actuelle
def get_engine():
    database_url = os.getenv("DATABASE_URL", "sqlite:///./db/mydatabase.db")
    return create_engine(database_url, connect_args={"check_same_thread": False})

# Initialisation de l'engine et de la session
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ShortenedURL.metadata.create_all(bind=engine)

# Fonction de réinitialisation de l'engine
def reset_engine():
    global engine
    engine = get_engine()  # Réinitialisation de l'engine
    SessionLocal.configure(bind=engine)  # Reconfigurer la session pour utiliser le nouvel engine
    ShortenedURL.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend React (port 5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAlchemy configuration for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./db/mydatabase.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Route to shorten a URL
@app.post("/api/shorten/", response_model=ShortenedURLResponse)
async def shorten_url(request: ShortenedURLCreate):
    # Check if the original URL already exists in the db
    db = SessionLocal()
    existing_entry = db.query(ShortenedURL).filter(ShortenedURL.original_url == request.original_url).first()
    if existing_entry:
        return ShortenedURLResponse(id=existing_entry.id, short_code=existing_entry.short_code, 
                                    original_url=existing_entry.original_url, title=existing_entry.title)

    # Create a non duplicate new shortcode
    short_code = generate_short_code()
    while db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first():
        short_code = generate_short_code()

    # Get the title of the original page
    try:
        response = requests.get(request.original_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
    except Exception:
        title = "No Title"

    # Save the new shortened URL in the database
    new_url = ShortenedURL(original_url=request.original_url, short_code=short_code, title=title)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return ShortenedURLResponse(id=new_url.id, short_code=new_url.short_code, original_url=new_url.original_url, title=new_url.title)

# Route to get the list of the shortened URLs
@app.get("/api/list/", response_model=list[ShortenedURLResponse])
async def list_short_urls():
    db = SessionLocal()
    shortlinks = db.query(ShortenedURL).order_by(ShortenedURL.id.desc()).all()
    return [ShortenedURLResponse(id=link.id, original_url=link.original_url, short_code=link.short_code, title=link.title) for link in shortlinks]

# Route to get the original URL from a shortcode
@app.get("/api/urls/{short_code}", response_model=ShortenedURLResponse)
async def get_original_url(short_code: str):
    db = SessionLocal()
    entry = db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first()
    if entry:
        return ShortenedURLResponse(id=entry.id, short_code=entry.short_code, original_url=entry.original_url, title=entry.title)
    raise HTTPException(status_code=404, detail="Shortlink not found")

# Home route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI with SQLite!",
        "description": "This API allows you to shorten URLs and retrieve original URLs using short codes.",
        "version": "1.0.0",
        "available_routes": {
            "/api/shorten/": "Create a short URL",
            "/api/urls/{short_code}/": "Retrieve the original URL for a given short code",
            "/api/list/": "Get the list of all shortened URLs",
        },
        "documentation": "Visit /docs for the full API documentation."
    }
