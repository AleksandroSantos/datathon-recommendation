from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.utils.helpers import load_data, save_data
from src.monitoring.logger import log

def handle_cold_start(news_title, items_data_path="data/raw/itens.csv", top_n=5):
    """
    Trata o problema de cold-start para notícias novas.
    
    Args:
        news_title (str): Título da nova notícia.
        items_data_path (str): Caminho para os dados dos itens.
        top_n (int): Número de recomendações a serem retornadas.
    
    Returns:
        list: IDs das notícias mais similares.
    """
    log("Carregando dados dos itens...")
    items_data = load_data(items_data_path)

    log("Calculando embeddings...")
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    news_embedding = model.encode([news_title])
    item_embeddings = model.encode(items_data['Title'].tolist())

    log("Calculando similaridade...")
    similarities = cosine_similarity(news_embedding, item_embeddings).flatten()
    top_indices = np.argsort(similarities)[-top_n:][::-1]

    log("Retornando notícias mais similares...")
    return items_data.iloc[top_indices]['Page'].tolist()

if __name__ == "__main__":
    # Exemplo de uso
    recommended_news = handle_cold_start("Novo lançamento da Globo")
    print(f"Notícias recomendadas: {recommended_news}")