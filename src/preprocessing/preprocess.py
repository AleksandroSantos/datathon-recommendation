import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from src.utils.helpers import save_data
from src.monitoring.logger import log

def preprocess_data(train_data_path, items_data_path, output_path):
    """
    Pré-processa os dados de treino e itens.
    
    Args:
        train_data_path (str): Caminho para os dados de treino.
        items_data_path (str): Caminho para os dados dos itens.
        output_path (str): Caminho para salvar os dados processados.
    """
    log("Carregando dados...")
    train_data = pd.read_parquet(train_data_path)
    items_data = pd.read_parquet(items_data_path)

    log("Realizando merge dos dados...")
    merged_data = pd.merge(train_data, items_data, left_on='history', right_on='page', how='left')

    log("Feature Engineering...")
    merged_data['timestampHistory'] = pd.to_numeric(merged_data['timestampHistory'], errors='coerce')
    merged_data['timestampHistory'] = pd.to_datetime(merged_data['timestampHistory'], unit='ms')
    # merged_data['Issued'] = pd.to_numeric(merged_data['Issued'], errors='coerce')
    merged_data['Issued'] = pd.to_datetime(merged_data['Issued'], unit='s')
    
    # merged_data['Issued'] = pd.to_datetime(merged_data['Issued'])
    merged_data['recency'] = (merged_data['timestampHistory'] - merged_data['Issued']).dt.days
    merged_data['recency_weight'] = np.exp(-merged_data['recency'] / 30)  # Decaimento em 30 dias

    log("Normalizando features...")
    scaler = MinMaxScaler()
    numeric_features = ['timeOnPageHistory', 'numberOfClicksHistory', 'scrollPercentageHistory', 'recency']
    merged_data[numeric_features] = scaler.fit_transform(merged_data[numeric_features])

    log("Salvando dados processados...")
    save_data(merged_data, output_path)

if __name__ == "__main__":
    preprocess_data(
        train_data_path="data/raw/interacoes.parquet",
        items_data_path="data/raw/noticias.parquet",
        output_path="data/processed/processed_data.parquet"
    )