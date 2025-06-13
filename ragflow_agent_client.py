# ragflow_agent_client.py
import requests
import json
from config import RAGFLOW_API_KEY, RAGFLOW_BASE_URL, RAGFLOW_AGENT_ID

class RagflowAgentClient:
    def __init__(self):
        self.base_url = RAGFLOW_BASE_URL
        self.token = RAGFLOW_API_KEY
        self.agent_id = RAGFLOW_AGENT_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.endpoint_url = f"{self.base_url}/api/v1/agents_openai/{self.agent_id}/chat/completions"

    def get_completion(self, user_query: str):
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_query}
            ],
            "stream": False
        }

        try:
            response = requests.post(self.endpoint_url, headers=self.headers, json=payload, timeout=180)
            response.raise_for_status()
            json_data = response.json()
            
            # Checa por erros de autenticação no corpo da resposta
            if json_data.get("code") == 109 and "invalid" in json_data.get("message", ""):
                 return f"ERRO DE AUTENTICAÇÃO: {json_data['message']}"

            final_answer = json_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if final_answer:
                return final_answer.strip()
            else:
                return f"Resposta recebida, mas sem conteúdo. Resposta completa: {json.dumps(json_data)}"

        except requests.exceptions.HTTPError as http_err:
            return f"Erro de HTTP: {http_err}. Resposta do servidor: {http_err.response.text}"
        except requests.exceptions.RequestException as e:
            return f"Erro de Conexão: {e}"