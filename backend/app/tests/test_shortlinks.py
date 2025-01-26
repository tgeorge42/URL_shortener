# app/tests/test_shortlinks.py

from app.main import app
from fastapi.testclient import TestClient
import os
import pytest
from backend.app.database.database import SessionLocal
from backend.app.models.models import ShortenedURL

client = TestClient(app)

# Create a shortlink and add in the db
def create_shortlink_in_db(original_url, short_code=None, title=None):
    db = SessionLocal()
    if not short_code:
        short_code = "W8etMM"
    short_url = ShortenedURL(original_url=original_url, short_code=short_code, title=title or "Test Title")
    db.add(short_url)
    db.commit()
    db.refresh(short_url)
    db.close()
    return short_url

# Test the creation of a shortlink
def test_create_shortlink():
    short_url = create_shortlink_in_db("https://example.com")
    
    try:
        response = client.post("/api/shorten/", json={"original_url": "https://example.com"})
        assert response.status_code == 200
        response_data = response.json()
        assert "short_code" in response_data
        assert response_data["original_url"] == "https://example.com"
    
    finally:
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.id == short_url.id).delete()
        db.commit()
        db.close()

# Test to get the original URL from the shortcode
def test_fetch_original_url():
    short_url = create_shortlink_in_db("https://docs.pytest.org/en/stable/", "W8etMM")
    
    try:
        response = client.get("/api/urls/W8etMM/")
        assert response.status_code == 200
        assert response.json()["original_url"] == "https://docs.pytest.org/en/stable/"
    
    finally:
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.id == short_url.id).delete()
        db.commit()
        db.close()

# Test if a non existent shortcodereturns 404
def test_fetch_non_existent_shortlink():
    try:
        response = client.get("/api/urls/NonExistentCode/")
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Shortlink not found"
    
    finally:
        pass

# Test the list of shortcodes
def test_list_shortlinks():
    short_url1 = create_shortlink_in_db("https://example1.com", "Code1", "Title 1")
    short_url2 = create_shortlink_in_db("https://example2.com", "Code2", "Title 2")
    
    try:
        response = client.get("/api/list/")
        assert response.status_code == 200
        data = response.json()

        assert any(item["short_code"] == "Code1" and item["original_url"] == "https://example1.com" and item["title"] == "Title 1" for item in data)
        assert any(item["short_code"] == "Code2" and item["original_url"] == "https://example2.com" and item["title"] == "Title 2" for item in data)

    finally:
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.short_code == "Code1").delete()
        db.query(ShortenedURL).filter(ShortenedURL.short_code == "Code2").delete()
        db.commit()
        db.close()

