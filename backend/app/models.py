# /app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class ShortenedURL(Base):
    __tablename__ = 'shortened_urls'
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, index=True)
    short_code = Column(String, unique=True, index=True)
    title = Column(String)
