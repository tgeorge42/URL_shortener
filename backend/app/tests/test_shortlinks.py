# app/tests/test_shortlinks.py

from app.main import app, reset_engine  # Assurez-vous que reset_engine est bien importée ici
from fastapi.testclient import TestClient
import os
import pytest
from app.database import Base, SessionLocal, engine
from app.models import ShortenedURL

@pytest.fixture(autouse=True)
def reset_database_url():
    # Sauvegarder l'ancienne valeur pour la restaurer après
    original_db_url = os.getenv("DATABASE_URL")
    
    # Changer l'URL de la base de données pour les tests
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    # Exécuter les tests
    yield
    
    # Réinitialiser après les tests pour éviter les effets secondaires
    if original_db_url:
        os.environ["DATABASE_URL"] = original_db_url
    else:
        del os.environ["DATABASE_URL"]  # Supprimer la variable si elle n'existait pas initialement

    # Réinitialiser l'engine après les tests
    reset_engine()

client = TestClient(app)

# Configure a temporary database for the tests
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.commit()
    db.close()

# Used to clean the db after each test
def teardown_database():
    Base.metadata.drop_all(bind=engine)

# Test the creation of shortlinks
def test_create_shortlink():
    setup_database()
    response = client.post("/api/shorten/", json={"original_url": "https://example.com"})
    assert response.status_code == 200
    response_data = response.json()
    assert "short_code" in response_data
    assert response_data["original_url"] == "https://example.com"
    teardown_database()

# Response test for fetch original URL
def test_fetch_original_url():
    setup_database()

    # Ajoute un lien raccourci à la base de données avant de tester la récupération
    db = SessionLocal()
    short_url = ShortenedURL(original_url="https://docs.pytest.org/en/stable/", short_code="W8etMM", title="Pytest Documentation")
    db.add(short_url)
    db.commit()
    db.refresh(short_url)  # Assure-toi que l'objet est bien enregistré
    db.close()

    # Teste la récupération de l'URL originale pour le short code "W8etMM"
    response = client.get("/api/urls/W8etMM/")

    assert response.status_code == 200
    assert response.json()["original_url"] == "https://docs.pytest.org/en/stable/"

    teardown_database()

# Test a non existent shortlink
def test_fetch_non_existent_shortlink():
    setup_database()

    response = client.get("/api/urls/NonExistentCode/")

    # Check if the status is 404 and if the return message is correct
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Shortlink not found"

    teardown_database()

# Test the list of shortcodes
def test_list_shortlinks():
    setup_database()

    # Create a couple shortened URLs in the db
    db = SessionLocal()
    links = [
        ShortenedURL(original_url="https://example1.com", short_code="Code1", title="Title 1"),
        ShortenedURL(original_url="https://example2.com", short_code="Code2", title="Title 2"),
    ]
    db.add_all(links)
    db.commit()
    db.close()

    # Check if the list is correct
    response = client.get("/api/list/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    teardown_database()
