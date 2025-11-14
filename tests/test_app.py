import pytest
import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))




@pytest.fixture
def client():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage_status_code(client):
    response = client.get("/")
    assert response.status_code == 200 # Vérifie que la route / renvoie bien un rendu valide


# Test sur l'affichage et l'éditions des vidéos
def test_video_not_found_returns_404(client):
    # On demande une vidéo avec un ID qui n'existe pas
    response = client.get("/videos/9999")

    assert response.status_code == 404     # Le code attendu est 404

def test_edit_video_not_found_returns_404(client):
    response = client.get("/videos/9999/edit")
    assert response.status_code == 404


# Test sur les filtres
def test_search_page_loads(client):
    response = client.get("/videos/search")
    
    assert response.status_code == 200
    assert b"Rechercher" in response.data
