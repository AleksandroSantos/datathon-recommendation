# tests/test_data_loader.py
import pytest
from unittest.mock import patch, MagicMock
from src.data.data_loader import DataLoader
import pandas as pd
import os

@patch('src.data.data_loader.pd.read_csv')
@patch('src.data.data_loader.glob')
def test_load_data_files_csv(mock_glob, mock_read_csv):
    mock_glob.return_value = ['data/transient/files/treino/treino_parte1.csv']
    mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    
    data_loader = DataLoader()
    df = data_loader.load_data_files('data/transient/files/treino/treino_parte*.csv')
    
    assert not df.empty
    mock_glob.assert_called_once_with('data/transient/files/treino/treino_parte*.csv')
    mock_read_csv.assert_called_once_with('data/transient/files/treino/treino_parte1.csv')

@patch('src.data.data_loader.pd.DataFrame.to_parquet')
def test_save_data(mock_to_parquet):
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    data_loader = DataLoader()
    data_loader.save_data(df, 'data/raw/interacoes.parquet')
    
    mock_to_parquet.assert_called_once_with('data/raw/interacoes.parquet', compression='snappy', index=False)