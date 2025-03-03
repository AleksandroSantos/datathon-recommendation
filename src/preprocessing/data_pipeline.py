import os
import pandas as pd
from glob import glob
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataLoader:
    def load_and_concat_files(self, file_pattern, file_type='csv'):
        """
        Carrega e concatena múltiplos arquivos CSV ou Parquet que correspondem a um padrão de nome.

        Args:
            file_pattern (str): Padrão de nome dos arquivos (ex: 'data/files/treino/treino_parte*.csv').
            file_type (str): Tipo de arquivo a ser carregado ('csv' ou 'parquet').

        Returns:
            pd.DataFrame: DataFrame concatenado com os dados de todos os arquivos.
        """
        # Encontra todos os arquivos que correspondem ao padrão
        file_paths = glob(file_pattern)
        
        # Verifica se há arquivos para carregar
        if not file_paths:
            raise FileNotFoundError(f"Nenhum arquivo encontrado para o padrão: {file_pattern}")
        
        # Carrega e concatena os arquivos
        dataframes = []
        for file_path in file_paths:
            try:
                logger.info(f"Carregando arquivo: {file_path}")
                if file_type == 'csv':
                    df = pd.read_csv(file_path)
                elif file_type == 'parquet':
                    df = pd.read_parquet(file_path)
                else:
                    raise ValueError(f"Tipo de arquivo não suportado: {file_type}")
                
                # Verifica se o DataFrame está vazio
                if df.empty:
                    logger.warning(f"O arquivo {file_path} está vazio.")
                else:
                    dataframes.append(df)
            except Exception as e:
                logger.error(f"Erro ao carregar o arquivo {file_path}: {e}")
                continue
        
        # Verifica se há DataFrames para concatenar
        if not dataframes:
            raise ValueError("Nenhum DataFrame válido foi carregado.")
        
        # Concatena todos os DataFrames
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        
        # Remove duplicatas
        logger.info("Removendo duplicatas...")
        concatenated_df = concatenated_df.drop_duplicates()
        
        return concatenated_df

    def save_to_parquet(self, df, output_path, compression='snappy'):
        """
        Salva um DataFrame no formato Parquet.

        Args:
            df (pd.DataFrame): DataFrame a ser salvo.
            output_path (str): Caminho completo do arquivo Parquet de saída.
            compression (str): Tipo de compressão a ser usada (ex: 'snappy', 'gzip').
        """
        try:
            # Cria o diretório de saída, se não existir
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                logger.info(f"Criando diretório: {output_dir}")
                os.makedirs(output_dir)
            
            # Salva o DataFrame em Parquet
            df.to_parquet(output_path, compression=compression, index=False)
            logger.info(f"DataFrame salvo em: {output_path} (compressão: {compression})")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo Parquet: {e}")
            raise

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Instancia o DataLoader
        data_loader = DataLoader()

        # Carrega e concatena os arquivos CSV de interações
        logger.info("Carregando e concatenando arquivos de interações...")
        interacoes = data_loader.load_and_concat_files('../data/transient/files/treino/treino_parte*.csv', file_type='csv')
        
        # Carrega e concatena os arquivos CSV de notícias
        logger.info("Carregando e concatenando arquivos de notícias...")
        noticias = data_loader.load_and_concat_files('../data/transient/itens/itens/itens-parte*.csv', file_type='csv')

        # Salva os DataFrames concatenados em Parquet na zona row
        logger.info("Salvando DataFrames em Parquet...")
        data_loader.save_to_parquet(interacoes, '../data/raw/interacoes.parquet', compression='snappy')
        data_loader.save_to_parquet(noticias, '../data/raw/noticias.parquet', compression='snappy')

        logger.info("Processo concluído com sucesso!")
    except Exception as e:
        logger.error(f"Erro durante a execução: {e}")