# src/api/endpoints.py
from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional, Dict
from src.models.recommender import NewsRecommendationSystem
from src.utils.logger import logger
from src.utils.config import Config

router = APIRouter()


@router.get("/", response_model=dict)
async def root(request: Request):
    """Endpoint raiz com informações básicas da API."""
    recommender = request.app.state.recommender
    return {
        "app": "G1 News Recommender",
        "status": "running",
        "model_status": "loaded" if recommender else "limited",
        "endpoints": [
            "/health",
            "/recommend/{user_id}",
            "/popular",
            "/recent",
            "/train-model",
            "/reload-model",
            "/add-new",
        ],
    }


@router.get("/health", response_model=dict)
async def health_check(request: Request):
    """Verifica a saúde da API."""
    recommender = request.app.state.recommender
    return {
        "status": "healthy",
        "model_status": "loaded" if recommender else "limited",
        "model_source": "local" if Config.MODEL_PATH.exists() else "none",
        "data_loaded": (
            "yes" if recommender and recommender.news_df is not None else "no"
        ),
    }


@router.get("/recommend/{user_id}", response_model=dict)
async def get_recommendations(user_id: str, request: Request, n: Optional[int] = 5):
    """Retorna recomendações personalizadas para um usuário."""
    recommender = request.app.state.recommender
    if not recommender:
        raise HTTPException(
            status_code=503, detail="Serviço indisponível. Modelo não carregado."
        )

    try:
        recommendations = recommender.get_user_recommendations(user_id, n)
        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "status": "success",
        }
    except ValueError as e:
        logger.error(f"Dados não carregados: {e}")
        raise HTTPException(status_code=503, detail=f"Dados não carregados: {e}")
    except Exception as e:
        logger.error(f"Erro ao gerar recomendações para o usuário {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar recomendações: {e}")


@router.get("/popular", response_model=dict)
async def get_popular_news(request: Request, n: Optional[int] = 5):
    """Retorna as notícias mais populares."""
    recommender = request.app.state.recommender
    if not recommender:
        raise HTTPException(
            status_code=503, detail="Serviço indisponível. Modelo não carregado."
        )

    try:
        logger.info("Obtendo notícias populares...")
        if recommender.news_df is None or recommender.popularity_scores is None:
            logger.error(
                "Dados não carregados. Execute load_data e prepare_data primeiro."
            )
            raise HTTPException(status_code=503, detail="Dados não carregados.")

        popular_news = recommender.get_popular_recommendations(n)
        logger.info(f"Notícias populares obtidas: {popular_news}")
        return {"popular_news": popular_news, "status": "success"}
    except Exception as e:
        logger.error(f"Erro ao obter notícias populares: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter notícias populares: {e}"
        )


@router.get("/recent", response_model=dict)
async def get_recent_news(request: Request, n: Optional[int] = 5):
    """Retorna as notícias mais recentes."""
    recommender = request.app.state.recommender
    if not recommender:
        raise HTTPException(
            status_code=503, detail="Serviço indisponível. Modelo não carregado."
        )

    try:
        logger.info("Obtendo notícias recentes...")
        recent_news = recommender.get_recent_news(
            n
        )  # Chama o método get_recent_news da classe
        logger.info(f"Notícias recentes obtidas: {recent_news}")
        return {"recent_news": recent_news, "status": "success"}
    except Exception as e:
        logger.error(f"Erro ao obter notícias recentes: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter notícias recentes: {e}"
        )


@router.post("/train-model", response_model=dict)
async def train_model(request: Request):
    """Treina o modelo a partir dos dados atuais."""
    new_recommender = NewsRecommendationSystem(data_dir=Config.DATA_DIR)
    if not new_recommender:
        raise HTTPException(
            status_code=503, detail="Serviço indisponível. Modelo não carregado."
        )

    try:
        logger.info("Iniciando treinamento do modelo...")
        new_recommender.train_model()  # Chama o método train_model da classe
        logger.info("Modelo treinado e salvo com sucesso.")
        return {"status": "success", "message": "Modelo treinado e salvo com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao treinar o modelo: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao treinar o modelo: {e}")


@router.get("/reload-model", response_model=dict)
async def reload_model(request: Request):
    """Recarrega o modelo a partir do diretório local."""
    try:
        logger.info("Recarregando modelo...")
        new_recommender = NewsRecommendationSystem.load_model(str(Config.MODEL_PATH))
        if new_recommender:
            request.app.state.recommender = new_recommender
            logger.info("Modelo recarregado com sucesso.")
            return {"status": "success", "message": "Modelo recarregado com sucesso."}
        else:
            logger.error("Falha ao recarregar o modelo.")
            return {"status": "error", "message": "Falha ao recarregar o modelo."}
    except Exception as e:
        logger.error(f"Erro ao recarregar o modelo: {e}")
        return {"status": "error", "message": f"Erro ao recarregar o modelo: {e}"}


@router.post("/add-news", response_model=dict)
async def add_news(request: Request, news: List[Dict]):
    """Adiciona novas notícias ao sistema."""
    recommender = request.app.state.recommender
    if not recommender:
        raise HTTPException(
            status_code=503, detail="Serviço indisponível. Modelo não carregado."
        )

    try:
        logger.info("Adicionando novas notícias...")
        recommender.add_news(news)  # Chama o método add_news da classe
        logger.info("Notícias adicionadas com sucesso.")
        return {"status": "success", "message": "Notícias adicionadas com sucesso."}
    except Exception as e:
        logger.error(f"Erro ao adicionar notícias: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar notícias: {e}")
