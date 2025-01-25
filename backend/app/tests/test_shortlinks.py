from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_shortlink():
    response = client.post("/shorten/", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert "short_code" in response.json()

def test_redirect_to_url():
    short_code = "W8etMM"  # Remplacez par un code court existant dans la DB
    response = client.get(f"/go/{short_code}/")
    assert response.status_code == 200
    assert "original_url" in response.json()

def test_list_shortlinks():
    response = client.get("/list/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
