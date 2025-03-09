# src/data/data_loader.py
import os
import pandas as pd
from glob import glob
from src.utils.logger import logger


class DataLoader:

    def load_data_files(
        self, file_pattern: str, drop_duplicates: bool = True
    ) -> pd.DataFrame:
        """
        Carrega e concatena múltiplos arquivos CSV ou Parquet.

        Args:
            file_pattern (str): Padrão de nome dos arquivos.
            drop_duplicates (bool): Se True, remove duplicatas.

        Returns:
            pd.DataFrame: DataFrame concatenado.
        """
        file_paths = glob(file_pattern)
        if not file_paths:
            raise FileNotFoundError(f"Nenhum arquivo encontrado para: {file_pattern}")

        dataframes = []
        for file_path in file_paths:
            try:
                logger.info(f"Carregando arquivo: {file_path}")
                if file_path.endswith(".csv"):
                    df = pd.read_csv(file_path)
                elif file_path.endswith(".parquet"):
                    df = pd.read_parquet(file_path)
                else:
                    raise ValueError(f"Formato não suportado: {file_path}")

                if df.empty:
                    logger.warning(f"Arquivo {file_path} está vazio.")
                else:
                    dataframes.append(df)
            except Exception as e:
                logger.error(f"Erro ao carregar {file_path}: {e}")
                continue

        if not dataframes:
            raise ValueError("Nenhum DataFrame válido foi carregado.")

        df_final = pd.concat(dataframes, ignore_index=True)
        return df_final.drop_duplicates() if drop_duplicates else df_final

    def save_data(
        self, df: pd.DataFrame, output_path: str, compression: str = "snappy"
    ) -> None:
        """
        Salva um DataFrame no formato Parquet.

        Args:
            df (pd.DataFrame): DataFrame a ser salvo.
            output_path (str): Caminho completo do arquivo Parquet de saída.
            compression (str): Tipo de compressão a ser usada (ex: 'snappy', 'gzip').
        """
        try:
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                logger.info(f"Criando diretório: {output_dir}")
                os.makedirs(output_dir)

            df.to_parquet(output_path, compression=compression, index=False)
            logger.info(
                f"DataFrame salvo em: {output_path} (compressão: {compression})"
            )
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo Parquet: {e}")
            raise


if __name__ == "__main__":
    try:
        # Instancia o DataLoader
        data_loader = DataLoader()

        # Carrega e concatena os arquivos CSV de interações
        logger.info("Carregando e concatenando arquivos de interações...")
        interacoes = data_loader.load_data_files(
            "data/transient/files/treino/treino_parte*.csv"
        )

        # Carrega e concatena os arquivos CSV de notícias
        logger.info("Carregando e concatenando arquivos de notícias...")
        noticias = data_loader.load_data_files(
            "data/transient/itens/itens/itens-parte*.csv"
        )

        # Salva os DataFrames concatenados em Parquet na zona raw
        logger.info("Salvando DataFrames em Parquet...")
        data_loader.save_data(
            interacoes, "data/raw/interacoes.parquet", compression="snappy"
        )
        data_loader.save_data(
            noticias, "data/raw/noticias.parquet", compression="snappy"
        )

        logger.info("Processo concluído com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")
