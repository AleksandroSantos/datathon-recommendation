# src/api/main.py
import uvicorn
from fastapi import FastAPI
from src.utils.logger import logger
from src.utils.config import Config
from src.api.endpoints import router as api_router
from src.models.recommender import NewsRecommendationSystem

# Cria a aplicação FastAPI
app = FastAPI(
    title="G1 News Recommender",
    description="API de recomendação de notícias do G1",
    version="1.0.0",
)

# Adiciona os endpoints
app.include_router(api_router)

# Instância do recomendador
recommender = None


@app.on_event("startup")
async def startup_event():
    """Carrega o modelo na inicialização da API."""
    global recommender
    try:
        if Config.MODEL_PATH.exists():
            logger.info("Carregando modelo local...")
            recommender = NewsRecommendationSystem.load_model(str(Config.MODEL_PATH))
            logger.info("Modelo carregado com sucesso.")
        else:
            logger.warning(
                "Nenhum modelo local encontrado. Iniciando em modo limitado."
            )
            recommender = NewsRecommendationSystem(data_dir=Config.DATA_DIR)
            logger.info("Carregando dados...")
            recommender.load_data()
            logger.info("Preparando dados...")
            recommender.prepare_data()
            logger.info("Dados carregados e preparados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}")
        logger.warning("API iniciada em modo limitado.")
        recommender = NewsRecommendationSystem(data_dir=Config.DATA_DIR)

    # Armazena o recommender no estado do app
    app.state.recommender = recommender


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
