# tests/test_endpoints.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.recommender import NewsRecommendationSystem
from src.utils.config import Config

@pytest.fixture
def client():
    return TestClient(app)

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "G1 News Recommender"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_recommendations(client):
    response = client.get("/recommend/user1")
    assert response.status_code == 200
    assert "recommendations" in response.json()