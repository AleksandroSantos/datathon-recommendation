# tests/conftest.py
import pytest
from src.models.recommender import NewsRecommendationSystem


@pytest.fixture
def recommender():
    return NewsRecommendationSystem(data_dir="fake_dir")
