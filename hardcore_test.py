# hardcode_test.py
import requests
import uuid
import json

print("--- INICIANDO TESTE COM CREDENCIAIS FIXAS NO CÓDIGO ---")

# =======================================================================
# !! IMPORTANTE !!
# Cole sua URL, sua CHAVE DE API e seu ID de Diálogo aqui,
# diretamente dentro das aspas.
# Certifique-se de que a CHAVE DE API é a que você acabou de
# gerar novamente na tela do RAGflow.

BASE_URL = "http://localhost"
API_KEY = "ragflow-I1NjJhNmEyNDcxNDExZjA4OTg5MGFjNm"
DIALOGUE_ID = "b4321522470811f08bc20ac6ecc7c6a1"
# =======================================================================

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
endpoint_url = f"{BASE_URL}/v1/canvas/completion"

payload = {
    "id": DIALOGUE_ID,
    "materia": "Este é o teste final e definitivo",
    "message_id": str(uuid.uuid4())
}

print(f"Enviando requisição para: {endpoint_url}")
print("-------------------------------------------------")

try:
    response = requests.post(endpoint_url, headers=headers, json=payload, timeout=20)
    print("\n--- RESPOSTA DO SERVIDOR ---")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("--------------------------")
except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro de conexão: {e}")