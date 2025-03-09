# src/utils/config.py
import os
from pathlib import Path


class Config:
    """Classe para carregar configurações do ambiente."""

    MODEL_DIR = os.getenv("MODEL_DIR", "data/models")
    DATA_DIR = os.getenv("DATA_DIR", "data")
    MODEL_PATH = Path(MODEL_DIR) / "recommendation_model.pkl"
    PORT = int(os.getenv("PORT", 8000))
    FILE_ID = os.getenv("FILE_ID", "13rvnyK5PJADJQgYe-VbdXb7PpLPj7lPr")
    OUTPUT_ZIP = os.getenv("OUTPUT_ZIP", "data.zip")
    DATA_DIR_TRANSIENT = os.getenv("DATA_DIR_TRANSIENT", "data/transient")
