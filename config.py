# config.py
import os
from dotenv import load_dotenv

load_dotenv()

RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
RAGFLOW_BASE_URL = os.getenv("RAGFLOW_BASE_URL")
RAGFLOW_DIALOGUE_ID = os.getenv("RAGFLOW_DIALOGUE_ID") # Adicione esta linha

if not RAGFLOW_API_KEY or not RAGFLOW_BASE_URL or not RAGFLOW_DIALOGUE_ID:
    raise ValueError(
        "Erro: Uma ou mais variáveis de ambiente (API_KEY, BASE_URL, DIALOGUE_ID) não foram encontradas no arquivo .env"
    )