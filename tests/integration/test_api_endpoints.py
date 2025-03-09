# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "app": "G1 News Recommender",
        "status": "running",
        "model_status": "limited",
        "endpoints": ["/recommend/{user_id}", "/popular", "/health", "/reload-model"],
    }


def test_recommend_endpoint(client):
    response = client.get("/recommend/user1")
    assert response.status_code == 200
    assert "recommendations" in response.json()


def test_popular_endpoint(client):
    response = client.get("/popular")
    assert response.status_code == 200
    assert "popular_news" in response.json()
