# ragflow_client.py
import requests
import uuid
import json
from config import RAGFLOW_API_KEY, RAGFLOW_BASE_URL, RAGFLOW_DIALOGUE_ID

class RagflowClient:
    """
    Cliente final e definitivo para interagir com a API do Ragflow.
    """
    def __init__(self):
        self.base_url = RAGFLOW_BASE_URL
        self.token = RAGFLOW_API_KEY
        self.dialogue_id = RAGFLOW_DIALOGUE_ID
        self.headers = {
            "Authorization": self.token, # Autenticação correta, sem "Bearer"
            "Content-Type": "application/json"
        }
        self.endpoint_url = f"{self.base_url}/v1/canvas/completion"

    def get_completion(self, user_query: str):
        """
        Envia uma consulta para o canvas do Ragflow e processa a resposta.
        """
        payload = {
            "id": self.dialogue_id,
            "message": user_query,
            "message_id": str(uuid.uuid4()),
            "running_hint_text": "is running...🕞"
        }

        try:
            with requests.post(self.endpoint_url, headers=self.headers, json=payload, stream=True, timeout=120) as response:
                response.raise_for_status()
                
                final_answer = ""
                raw_chunks_for_debug = []

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        raw_chunks_for_debug.append(decoded_line) # Guarda o chunk para depuração

                        if decoded_line.startswith("data:"):
                            json_str = decoded_line[len("data: "):]
                            if json_str.strip() and json_str.strip() != "[DONE]":
                                try:
                                    json_data = json.loads(json_str)
                                    # Se a resposta for um erro do servidor, mostre-o
                                    if json_data.get("code") == 500 and "message" in json_data:
                                        return f"Ocorreu um erro no servidor Ragflow: {json_data['message']}"

                                    # Tenta extrair a resposta de campos comuns
                                    if "message" in json_data and isinstance(json_data["message"], str):
                                        final_answer += json_data["message"]
                                    elif "answer" in json_data and isinstance(json_data["answer"], str):
                                        final_answer += json_data["answer"]
                                    elif "content" in json_data and isinstance(json_data["content"], str):
                                        final_answer += json_data["content"]
                                        
                                except json.JSONDecodeError:
                                    pass # Ignora linhas que não são JSON válido

                if not final_answer.strip():
                    # Se não encontrou a resposta, mostra os dados brutos para análise
                    return (f"--- DEBUG FINAL ---\n"
                            f"Conexão bem-sucedida, mas não foi possível extrair a resposta.\n"
                            f"Chunks brutos recebidos do servidor:\n\n" + "\n".join(raw_chunks_for_debug))
                
                return final_answer

        except requests.exceptions.HTTPError as http_err:
            return f"Erro de HTTP: {http_err}."
        except requests.exceptions.RequestException as e:
            return f"Erro de Conexão: {e}"