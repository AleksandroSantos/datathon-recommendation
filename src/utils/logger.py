# src/utils/logger.py
import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com formatação padrão.

    Args:
        name (str): Nome do logger.

    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Configura o handler para stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Cria o logger padrão
logger = setup_logger(__name__)
