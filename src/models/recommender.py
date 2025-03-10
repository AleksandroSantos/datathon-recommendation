# src/models/recommender.py
import pickle
from datetime import datetime, timedelta
from typing import Tuple, List, Dict

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.logger import logger
from src.utils.config import Config


class NewsRecommendationSystem:
    def __init__(
        self,
        data_dir: str = Config.DATA_DIR,
        max_features: int = 5000,
        decay_factor: float = 0.1,
    ):
        self.data_dir = Path(data_dir)
        self.max_features = max_features
        self.decay_factor = decay_factor
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        self.news_df = None
        self.user_df = None
        self.tfidf_matrix = None
        self.popularity_scores = None

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Carrega os dados de notícias e usuários."""
        news_path = self.data_dir / "raw/noticias.parquet"
        user_path = self.data_dir / "raw/interacoes.parquet"

        logger.info("Carregando dados de notícias e usuários...")
        self.news_df = pd.read_parquet(news_path).drop_duplicates(subset=["page"])
        self.user_df = pd.read_parquet(user_path).drop_duplicates(subset=["userId"])

        self._handle_missing_data()
        self.news_df["date"] = pd.to_datetime(
            self.news_df.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        logger.info("Dados carregados e validados com sucesso.")
        return self.news_df, self.user_df

    def _handle_missing_data(self) -> None:
        """Trata dados ausentes nas colunas críticas."""
        logger.info("Tratando dados ausentes...")
        self.news_df["title"] = self.news_df["title"].fillna("")
        self.news_df["body"] = self.news_df["body"].fillna("")
        self.news_df["caption"] = self.news_df["caption"].fillna("")
        self.user_df["history"] = self.user_df["history"].fillna("")

    def prepare_data(self) -> None:
        """Prepara os dados para recomendação."""
        logger.info("Preparando dados...")
        self._create_content_column()
        self._compute_tfidf_matrix()
        self._calculate_popularity_scores()
        logger.info("Dados preparados com sucesso.")

    def _create_content_column(self) -> None:
        """Cria a coluna 'content' combinando título, corpo e legenda."""
        self.news_df["content"] = self.news_df.apply(
            lambda x: f"{x['title']} {x['body']} {x.get('caption', '')}", axis=1
        )

    def _compute_tfidf_matrix(self) -> None:
        """Calcula a matriz TF-IDF para o conteúdo das notícias."""
        logger.info("Calculando matriz TF-IDF...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.news_df["content"])

    def _calculate_popularity_scores(self) -> None:
        """Calcula os scores de popularidade das notícias."""
        logger.info("Calculando scores de popularidade...")
        history = self.user_df["history"].str.split(",").explode().str.strip()
        view_counts = history.value_counts()
        self.popularity_scores = view_counts.apply(
            lambda x: x * self._calculate_time_decay(x)
        )
        self.popularity_scores /= self.popularity_scores.max()

    @staticmethod
    def _calculate_time_decay(date_series: pd.Series) -> pd.Series:
        """Aplica decaimento temporal aos scores de popularidade."""
        days_since = (datetime.now() - pd.to_datetime(date_series)).days
        return 1 / (1 + 0.1 * max(days_since, 0))

    def get_recommendations_for_new_user(self, n: int = 5) -> List[Dict]:
        """Recomenda notícias para novos usuários."""
        self.news_df["popularity_score"] = (
            self.news_df["page"].map(self.popularity_scores).fillna(0)
        )

        # Notícias recentes e populares
        recent_cutoff = datetime.now() - timedelta(days=2)
        recent_news = self.news_df[self.news_df["date"] >= recent_cutoff].nlargest(
            n // 2, "popularity_score"
        )
        all_time_news = self.news_df.nlargest(n // 2, "popularity_score")

        recommended_news = (
            pd.concat([recent_news, all_time_news]).drop_duplicates().head(n)
        )
        return recommended_news.to_dict(orient="records")

    def get_user_recommendations(self, user_id: str, n: int = 5) -> List[Dict]:
        """Recomenda notícias personalizadas para um usuário."""
        if self.news_df is None or self.user_df is None:
            raise ValueError(
                "Dados não carregados. Execute o método load_data primeiro."
            )

        user = self.user_df[self.user_df["userId"] == user_id]
        if user.empty or user.iloc[0]["historySize"] == 0:
            return self.get_recommendations_for_new_user(n)

        history = user.iloc[0]["history"].split(",")
        last_article = history[-1]
        content_recs = self._get_content_based_recommendations(last_article, n)
        popular_recs = self._get_popular_recommendations(n)
        return sorted(
            content_recs + popular_recs, key=lambda x: x["score"], reverse=True
        )[:n]

    def _get_content_based_recommendations(
        self, article_id: str, n: int = 5
    ) -> List[Dict]:
        """Recomenda notícias baseadas em similaridade de conteúdo."""
        try:
            idx = self.news_df[self.news_df["page"] == article_id].index[0]
            similarities = cosine_similarity(
                self.tfidf_matrix[idx], self.tfidf_matrix
            ).flatten()
            similar_indices = similarities.argsort()[-n - 1 : -1][::-1]
            return self.news_df.iloc[similar_indices][["page", "title", "url"]].to_dict(
                orient="records"
            )
        except Exception as e:
            logger.error(f"Erro ao buscar recomendações baseadas em conteúdo: {e}")
            return []

    def get_popular_recommendations(self, n: int = 5) -> List[Dict]:
        """Recomenda notícias populares."""
        if self.popularity_scores is None:
            raise ValueError(
                "Scores de popularidade não calculados. Execute prepare_data primeiro."
            )

        # Adiciona a coluna 'popularity_score' ao DataFrame, se ainda não existir
        if "popularity_score" not in self.news_df.columns:
            self.news_df["popularity_score"] = (
                self.news_df["page"].map(self.popularity_scores).fillna(0)
            )

        # Retorna as n notícias mais populares
        return self.news_df.nlargest(n, "popularity_score")[
            ["page", "title", "url"]
        ].to_dict(orient="records")

    def save_model(self) -> None:
        """Salva o modelo no caminho especificado."""
        model_path = self.data_dir / "models/recommendation_model.pkl"
        model_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Salvando modelo em {model_path}...")
        with open(model_path, "wb") as f:
            pickle.dump(
                {
                    "news_df": self.news_df,
                    "user_df": self.user_df,
                    "tfidf_matrix": self.tfidf_matrix,
                    "popularity_scores": self.popularity_scores,
                },
                f,
            )
        logger.info("Modelo salvo com sucesso.")

    @classmethod
    def load_model(cls, path: str):
        """Carrega o modelo salvo."""
        with open(path, "rb") as f:
            data = pickle.load(f)
            instance = cls(data_dir="")
            instance.news_df = data["news_df"]
            instance.user_df = data["user_df"]
            instance.tfidf_matrix = data["tfidf_matrix"]
            instance.popularity_scores = data["popularity_scores"]
            return instance

    def train_model(self) -> None:
        """Treina o modelo a partir dos dados atuais."""

        logger.info("Inicializando o sistema de recomendação...")
        self.load_data()

        logger.info("Preparando dados...")
        self.prepare_data()

        logger.info("Salvando o modelo...")
        self.save_model()

    def add_news(self, news: List[Dict]) -> None:
        """Adiciona novas notícias ao sistema."""
        new_news_df = pd.DataFrame(news)
        self.news_df = pd.concat([self.news_df, new_news_df], ignore_index=True)

    def get_recent_news(self, n: int = 5) -> List[Dict]:
        """Retorna as notícias mais recentes."""
        recent_cutoff = datetime.now() - timedelta(
            days=2
        )  # Notícias dos últimos 2 dias
        recent_news = self.news_df[self.news_df["date"] >= recent_cutoff].head(n)
        return recent_news[["page", "title", "url"]].to_dict(orient="records")
