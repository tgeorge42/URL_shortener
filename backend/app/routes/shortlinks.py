# /app/routes/shortlinks.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..models import ShortenedURL
from ..schemas import ShortenedURLCreate, ShortenedURLResponse
import requests
from bs4 import BeautifulSoup
import random
import string

router = APIRouter()

# Fonction pour générer un shortcode
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Route pour raccourcir une URL
@router.post("/shorten/", response_model=ShortenedURLResponse)
async def shorten_url(request: ShortenedURLCreate, db: Session = Depends(database.get_db)):
    # Vérifier si l'URL originale existe déjà dans la base de données
    existing_entry = db.query(ShortenedURL).filter(ShortenedURL.original_url == request.original_url).first()
    if existing_entry:
        return ShortenedURLResponse(id=existing_entry.id, short_code=existing_entry.short_code, 
                                    original_url=existing_entry.original_url, title=existing_entry.title)

    # Créer un shortcode non dupliqué
    short_code = generate_short_code()
    while db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first():
        short_code = generate_short_code()

    # Récupérer le titre de la page originale
    try:
        response = requests.get(request.original_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
    except Exception:
        title = "No Title"

    # Sauvegarder la nouvelle URL raccourcie dans la base de données
    new_url = ShortenedURL(original_url=request.original_url, short_code=short_code, title=title)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return ShortenedURLResponse(id=new_url.id, short_code=new_url.short_code, original_url=new_url.original_url, title=new_url.title)

# Route pour obtenir la liste des URLs raccourcies
@router.get("/list/", response_model=list[ShortenedURLResponse])
async def list_short_urls(db: Session = Depends(database.get_db)):
    shortlinks = db.query(ShortenedURL).order_by(ShortenedURL.id.desc()).all()
    return [ShortenedURLResponse(id=link.id, original_url=link.original_url, short_code=link.short_code, title=link.title) for link in shortlinks]

# Route pour obtenir l'URL originale à partir d'un shortcode
@router.get("/urls/{short_code}", response_model=ShortenedURLResponse)
async def get_original_url(short_code: str, db: Session = Depends(database.get_db)):
    entry = db.query(ShortenedURL).filter(ShortenedURL.short_code == short_code).first()
    if entry:
        return ShortenedURLResponse(id=entry.id, short_code=entry.short_code, original_url=entry.original_url, title=entry.title)
    raise HTTPException(status_code=404, detail="Shortlink not found")
