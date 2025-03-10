# tests/test_recommender.py
import pytest
from unittest.mock import patch, MagicMock
from src.models.recommender import NewsRecommendationSystem
import pandas as pd
import numpy as np


@patch("src.models.recommender.pd.read_parquet")
def test_load_data(mock_read_parquet):
    mock_read_parquet.side_effect = [
        pd.DataFrame(
            {
                "page": ["page1", "page2"],
                "title": ["title1", "title2"],
                "body": ["body1", "body2"],  # Adiciona a coluna 'body'
                "caption": ["caption1", "caption2"],  # Adiciona a coluna 'caption'
            }
        ),
        pd.DataFrame(
            {"userId": ["user1", "user2"], "history": ["page1,page2", "page2"]}
        ),
    ]

    recommender = NewsRecommendationSystem()
    news_df, user_df = recommender.load_data()

    assert not news_df.empty
    assert not user_df.empty


@patch("src.models.recommender.NewsRecommendationSystem._compute_tfidf_matrix")
@patch("src.models.recommender.NewsRecommendationSystem._calculate_popularity_scores")
def test_prepare_data(mock_calculate_popularity, mock_compute_tfidf):
    recommender = NewsRecommendationSystem()
    recommender.news_df = pd.DataFrame(
        {
            "page": ["page1", "page2"],
            "title": ["title1", "title2"],
            "body": ["body1", "body2"],  # Adiciona a coluna 'body'
            "caption": ["caption1", "caption2"],  # Adiciona a coluna 'caption'
        }
    )
    recommender.user_df = pd.DataFrame(
        {"userId": ["user1", "user2"], "history": ["page1,page2", "page2"]}
    )

    recommender.prepare_data()

    mock_compute_tfidf.assert_called_once()
    mock_calculate_popularity.assert_called_once()
