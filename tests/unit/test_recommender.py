# tests/unit/test_recommender.py
import pytest
import pandas as pd
from src.models.recommender import NewsRecommendationSystem


@pytest.fixture
def sample_data():
    news_data = pd.DataFrame(
        {
            "page": ["news1", "news2", "news3"],
            "title": ["Title 1", "Title 2", "Title 3"],
            "body": ["Body 1", "Body 2", "Body 3"],
            "caption": ["Caption 1", "Caption 2", "Caption 3"],
            "date": ["2023-10-01", "2023-10-02", "2023-10-03"],
        }
    )
    user_data = pd.DataFrame(
        {
            "userId": ["user1", "user2"],
            "history": ["news1,news2", "news3"],
            "historySize": [2, 1],
        }
    )
    return news_data, user_data


def test_load_data(sample_data):
    news_data, user_data = sample_data
    recommender = NewsRecommendationSystem(data_dir="fake_dir")

    # Simula a leitura de arquivos Parquet
    recommender.news_df = news_data
    recommender.user_df = user_data

    # Verifica se os dados foram carregados corretamente
    assert recommender.news_df is not None
    assert recommender.user_df is not None


def test_get_recommendations_for_new_user(sample_data):
    news_data, user_data = sample_data
    recommender = NewsRecommendationSystem(data_dir="fake_dir")
    recommender.news_df = news_data
    recommender.user_df = user_data

    recommendations = recommender.get_recommendations_for_new_user(n=2)
    assert len(recommendations) == 2
