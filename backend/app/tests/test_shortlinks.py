# app/tests/test_shortlinks.py

from app.main import app
from fastapi.testclient import TestClient
import os
import pytest
from app.database import SessionLocal
from app.models import ShortenedURL

client = TestClient(app)

# Fonction pour ajouter un enregistrement et suivre son ID
def create_shortlink_in_db(original_url, short_code=None, title=None):
    db = SessionLocal()
    if not short_code:
        short_code = "W8etMM"  # Un code par défaut
    short_url = ShortenedURL(original_url=original_url, short_code=short_code, title=title or "Test Title")
    db.add(short_url)
    db.commit()
    db.refresh(short_url)  # Assure-toi que l'objet est bien enregistré
    db.close()
    return short_url  # Retourner l'objet créé pour le nettoyage

# Test de création d'un shortlink
def test_create_shortlink():
    # Ajouter un enregistrement
    short_url = create_shortlink_in_db("https://example.com")
    
    try:
        response = client.post("/api/shorten/", json={"original_url": "https://example.com"})
        assert response.status_code == 200
        response_data = response.json()
        assert "short_code" in response_data
        assert response_data["original_url"] == "https://example.com"
    
    finally:
        # Supprimer uniquement l'entrée ajoutée pour ce test
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.id == short_url.id).delete()
        db.commit()
        db.close()

# Test de la récupération de l'URL originale
def test_fetch_original_url():
    # Ajouter un lien raccourci à la base de données
    short_url = create_shortlink_in_db("https://docs.pytest.org/en/stable/", "W8etMM")
    
    try:
        # Teste la récupération de l'URL originale pour le short code "W8etMM"
        response = client.get("/api/urls/W8etMM/")
        assert response.status_code == 200
        assert response.json()["original_url"] == "https://docs.pytest.org/en/stable/"
    
    finally:
        # Supprimer l'entrée ajoutée pendant le test
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.id == short_url.id).delete()
        db.commit()
        db.close()

# Test d'un shortlink inexistant
def test_fetch_non_existent_shortlink():
    try:
        response = client.get("/api/urls/NonExistentCode/")
        # Vérifier que le statut est 404 et que le message de retour est correct
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Shortlink not found"
    
    finally:
        # Aucune entrée créée, donc pas de suppression nécessaire
        pass

# Test de la liste des shortcodes
def test_list_shortlinks():
    # Créer des liens raccourcis spécifiques pour ce test
    short_url1 = create_shortlink_in_db("https://example1.com", "Code1", "Title 1")
    short_url2 = create_shortlink_in_db("https://example2.com", "Code2", "Title 2")
    
    try:
        # Vérifier la liste des liens raccourcis
        response = client.get("/api/list/")
        assert response.status_code == 200
        data = response.json()

        # Vérification des données dans la réponse
        assert any(item["short_code"] == "Code1" and item["original_url"] == "https://example1.com" and item["title"] == "Title 1" for item in data)
        assert any(item["short_code"] == "Code2" and item["original_url"] == "https://example2.com" and item["title"] == "Title 2" for item in data)

    finally:
        # Supprimer uniquement les données créées pendant ce test
        db = SessionLocal()
        db.query(ShortenedURL).filter(ShortenedURL.short_code == "Code1").delete()
        db.query(ShortenedURL).filter(ShortenedURL.short_code == "Code2").delete()
        db.commit()
        db.close()

