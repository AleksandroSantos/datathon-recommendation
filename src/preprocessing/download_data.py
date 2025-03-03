#!/usr/bin/env python
# coding: utf-8

import os
import requests
import zipfile
import logging
import gdown

# Configuração do logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constantes
FILE_ID = "13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr"
DOWNLOAD_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
OUTPUT_ZIP = "data.zip"
DATA_DIR = "../data/transient"
CHUNK_SIZE = 8192  # Tamanho dos chunks para download


def download_with_gdown():
    """Faz o download do arquivo usando gdown."""
    logger.info("Iniciando o download do arquivo com gdown...")
    try:
        # URL do Google Drive
        url = f"https://drive.google.com/uc?id={FILE_ID}"

        # Faz o download
        gdown.download(url, OUTPUT_ZIP, quiet=False)

        # Verifica o tamanho do arquivo baixado
        file_size = os.path.getsize(OUTPUT_ZIP)
        logger.info(
            f"Download concluído: {OUTPUT_ZIP} ({file_size / (1024 * 1024):.2f} MB)"
        )
    except Exception as e:
        logger.error(f"Erro ao fazer o download com gdown: {e}")
        raise


def extract_zip_file():
    """Extrai o conteúdo do arquivo zip para o diretório de dados."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    logger.info(f"Extraindo {OUTPUT_ZIP} para {DATA_DIR}...")
    try:
        with zipfile.ZipFile(OUTPUT_ZIP, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)
            logger.info("Arquivos extraídos:")
            for file in zip_ref.namelist():
                logger.info(f" - {file}")
        logger.info("Extração concluída.")
    except zipfile.BadZipFile:
        logger.error(f"O arquivo {OUTPUT_ZIP} não é um arquivo zip válido.")
        raise
    except Exception as e:
        logger.error(f"Erro ao extrair o arquivo: {e}")
        raise


def remove_zip_file():
    """Remove o arquivo zip após a extração."""
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)
        logger.info(f"Arquivo {OUTPUT_ZIP} removido.")


def main():
    """Função principal que orquestra o download, extração e limpeza."""
    try:
        download_with_gdown()
        extract_zip_file()
        remove_zip_file()
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise


if __name__ == "__main__":
    main()
