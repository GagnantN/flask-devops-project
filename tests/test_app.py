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
