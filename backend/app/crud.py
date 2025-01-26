from sqlalchemy.orm import Session
from . import models
import random, string

def create_shortened_url(db: Session, url: str) -> models.ShortenedURL:
    existing_entry = db.query(models.ShortenedURL).filter(models.ShortenedURL.original_url == url).first()
    if existing_entry:
        return existing_entry

    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    title = "No Title"

    db_url = models.ShortenedURL(original_url=url, short_code=short_code, title=title)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_shortened_url(db: Session, short_code: str):
    return db.query(models.ShortenedURL).filter(models.ShortenedURL.short_code == short_code).first()

def get_all_shortened_urls(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ShortenedURL).offset(skip).limit(limit).all()
