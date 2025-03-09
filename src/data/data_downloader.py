# src/data/data_downloader.py
import os
import zipfile
import gdown
from src.utils.logger import logger
from src.utils.config import Config


def download_file() -> None:
    """Faz o download do arquivo usando gdown."""
    logger.info("Iniciando o download do arquivo com gdown...")
    try:
        url = f"https://drive.google.com/uc?id={Config.FILE_ID}"
        gdown.download(url, Config.OUTPUT_ZIP, quiet=False)
        file_size = os.path.getsize(Config.OUTPUT_ZIP)
        logger.info(
            f"Download concluído: {Config.OUTPUT_ZIP} ({file_size / (1024 * 1024):.2f} MB)"
        )
    except Exception as e:
        logger.error(f"Erro ao fazer o download com gdown: {e}")
        raise


def extract_data():
    """Extrai o conteúdo do arquivo zip para o diretório de dados."""
    if not os.path.exists(Config.DATA_DIR_TRANSIENT):
        os.makedirs(Config.DATA_DIR_TRANSIENT)

    logger.info(f"Extraindo {Config.OUTPUT_ZIP} para {Config.DATA_DIR_TRANSIENT}...")
    try:
        with zipfile.ZipFile(Config.OUTPUT_ZIP, "r") as zip_ref:
            zip_ref.extractall(Config.DATA_DIR_TRANSIENT)
            logger.info("Arquivos extraídos:")
            for file in zip_ref.namelist():
                logger.info(f" - {file}")
        logger.info("Extração concluída.")
    except zipfile.BadZipFile:
        logger.error(f"O arquivo {Config.OUTPUT_ZIP} não é um arquivo zip válido.")
        raise
    except Exception as e:
        logger.error(f"Erro ao extrair o arquivo: {e}")
        raise


def cleanup_downloaded_file():
    """Remove o arquivo zip após a extração."""
    if os.path.exists(Config.OUTPUT_ZIP):
        os.remove(Config.OUTPUT_ZIP)
        logger.info(f"Arquivo {Config.OUTPUT_ZIP} removido.")


def main():
    """Função principal que orquestra o download, extração e limpeza."""
    try:
        download_file()
        extract_data()
        cleanup_downloaded_file()
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise


if __name__ == "__main__":
    main()
