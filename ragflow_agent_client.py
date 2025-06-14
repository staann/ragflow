# ragflow_agent_client.py (VERSÃO FINAL E FUNCIONAL)
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
        # Monta o payload para o RAGflow
        payload = {
            "model": "gpt-3.5-turbo", # Este campo é ignorado pelo RAGflow, mas necessário no formato
            "messages": [
                {"role": "user", "content": user_query}
            ],
            # --- CORREÇÃO PRINCIPAL: DESATIVANDO O STREAMING PARA EVITAR O BUG DO SERVIDOR ---
            "stream": False
        }

        try:
            # Aumentamos o timeout para dar tempo ao LLM de processar
            response = requests.post(self.endpoint_url, headers=self.headers, json=payload, timeout=180)
            
            response.raise_for_status() # Irá gerar um erro para status 4xx ou 5xx

            json_data = response.json()
            
            # Extrai o conteúdo da resposta completa no formato OpenAI não-streaming
            final_answer = json_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if final_answer:
                return final_answer.strip()
            else:
                return f"Resposta recebida, mas sem conteúdo. Resposta completa: {json.dumps(json_data)}"

        except requests.exceptions.HTTPError as http_err:
            return f"Erro de HTTP: {http_err}. Resposta do servidor: {http_err.response.text}"
        except requests.exceptions.RequestException as e:
            return f"Erro de Conexão: {e}"