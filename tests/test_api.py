# tests/test_api.py
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.recommender import NewsRecommendationSystem
from src.utils.config import Config


# Fixture para o cliente de teste
@pytest.fixture
def client():
    return TestClient(app)


# Fixture para simular o recommender
@pytest.fixture
def mock_recommender():
    # Cria uma instância do NewsRecommendationSystem
    recommender = NewsRecommendationSystem()

    # Simula os DataFrames de notícias e usuários
    recommender.news_df = pd.DataFrame(
        {
            "page": ["page1", "page2"],
            "title": ["title1", "title2"],
            "body": ["body1", "body2"],
            "caption": ["caption1", "caption2"],
            "date": ["2023-10-01", "2023-10-02"],
        }
    )
    recommender.user_df = pd.DataFrame(
        {"userId": ["user1", "user2"], "history": ["page1,page2", "page2"]}
    )

    # Prepara os dados (calcula TF-IDF e scores de popularidade)
    recommender.prepare_data()

    return recommender


# Teste para o endpoint raiz
def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert "status" in data
    assert "model_status" in data
    assert "endpoints" in data


# Teste para o endpoint de health check
def test_health_check(client, mock_recommender):
    # Substitui o recommender no estado do app pelo mock
    app.state.recommender = mock_recommender
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_status" in data
    assert "model_source" in data
    assert "data_loaded" in data


# Teste para o endpoint de recomendações
def test_get_recommendations(client, mock_recommender):
    app.state.recommender = mock_recommender
    response = client.get("/recommend/user1")
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "recommendations" in data
    assert "status" in data


# Teste para o endpoint de notícias populares
def test_get_popular_news(client, mock_recommender):
    app.state.recommender = mock_recommender
    response = client.get("/popular")
    assert response.status_code == 200
    data = response.json()
    assert "popular_news" in data
    assert "status" in data


# Teste para o endpoint de notícias recentes
def test_get_recent_news(client, mock_recommender):
    app.state.recommender = mock_recommender
    response = client.get("/recent")
    assert response.status_code == 200
    data = response.json()
    assert "recent_news" in data
    assert "status" in data


# Teste para o endpoint de treinamento do modelo
def test_train_model(client, mock_recommender):
    app.state.recommender = mock_recommender
    response = client.post("/train-model")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data


# Teste para o endpoint de adicionar notícias
def test_add_news(client, mock_recommender):
    app.state.recommender = mock_recommender
    new_news = [
        {
            "page": "page3",
            "title": "title3",
            "body": "body3",
            "caption": "caption3",
            "date": "2023-10-03",
        }
    ]
    response = client.post("/add-news", json={"news": new_news})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
