# train_and_save_model.py
from src.models.recommender import NewsRecommendationSystem
from src.utils.config import Config


def main():
    recommendation_system = NewsRecommendationSystem(data_dir=Config.DATA_DIR)
    recommendation_system.train_model()


if __name__ == "__main__":
    main()
