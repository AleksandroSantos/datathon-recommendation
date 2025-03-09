# tests/unit/test_data_loader.py
import pytest
import pandas as pd
from src.data.data_loader import DataLoader


def test_load_and_concat_files(tmpdir):
    # Cria arquivos CSV de teste
    df1 = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df2 = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})

    file1 = tmpdir.join("file1.csv")
    file2 = tmpdir.join("file2.csv")
    df1.to_csv(file1, index=False)
    df2.to_csv(file2, index=False)

    # Testa a função load_and_concat_files
    data_loader = DataLoader()
    result = data_loader.load_data_files(str(tmpdir.join("file*.csv")))

    # Verifica o resultado
    expected = pd.concat([df1, df2], ignore_index=True)
    pd.testing.assert_frame_equal(result, expected)


def test_save_to_parquet(tmpdir):
    # Cria um DataFrame de teste
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    # Testa a função save_to_parquet
    data_loader = DataLoader()
    output_path = str(tmpdir.join("output.parquet"))
    data_loader.save_to_parquet(df, output_path)

    # Verifica se o arquivo foi salvo corretamente
    saved_df = pd.read_parquet(output_path)
    pd.testing.assert_frame_equal(saved_df, df)
