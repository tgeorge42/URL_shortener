from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

# Route pour créer un shortlink
@router.post("/shorten/", response_model=schemas.ShortenedURLResponse)
def shorten_url(url: str, db: Session = Depends(database.get_db)):
    db_url = crud.create_shortened_url(db, url)
    return db_url

# Route pour récupérer le lien original depuis le shortlink
@router.get("/go/{short_code}/")
def redirect_to_url(short_code: str, db: Session = Depends(database.get_db)):
    db_url = crud.get_shortened_url(db, short_code)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Shortlink not found")
    return {"original_url": db_url.original_url}

# Route pour lister tous les shortlinks
@router.get("/list/")
def list_shortlinks(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    shortlinks = crud.get_all_shortened_urls(db, skip=skip, limit=limit)
    return shortlinks
