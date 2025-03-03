import pandas as pd
import joblib
import os
from src.monitoring.logger import log

def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega dados de um arquivo CSV.
    
    Args:
        file_path (str): Caminho para o arquivo CSV.
    
    Returns:
        pd.DataFrame: DataFrame com os dados carregados.
    """
    log(f"Carregando dados de {file_path}...")
    return pd.read_csv(file_path)

def save_data(data: pd.DataFrame, file_path: str):
    """
    Salva um DataFrame em um arquivo CSV.
    
    Args:
        data (pd.DataFrame): DataFrame a ser salvo.
        file_path (str): Caminho para salvar o arquivo CSV.
    """
    log(f"Salvando dados em {file_path}...")
    data.to_parquet(file_path, index=False)

def load_model(file_path: str):
    """
    Carrega um modelo salvo em um arquivo.
    
    Args:
        file_path (str): Caminho para o arquivo do modelo.
    
    Returns:
        Modelo carregado.
    """
    log(f"Carregando modelo de {file_path}...")
    return joblib.load(file_path)

def save_model(model, file_path: str):
    """
    Salva um modelo em um arquivo.
    
    Args:
        model: Modelo a ser salvo.
        file_path (str): Caminho para salvar o arquivo do modelo.
    """
    log(f"Salvando modelo em {file_path}...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(model, file_path)

def ensure_dir(directory: str):
    """
    Garante que um diretório existe. Se não existir, cria o diretório.
    
    Args:
        directory (str): Caminho do diretório.
    """
    if not os.path.exists(directory):
        log(f"Criando diretório {directory}...")
        os.makedirs(directory)