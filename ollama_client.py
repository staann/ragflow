# ollama_client.py
import requests
import os

class OllamaClient:
    """
    Um cliente para interagir com um modelo de linguagem Ollama.
    """
    def __init__(self, model_name, host='http://localhost:11434'):
        """
        Inicializa o cliente com o nome do modelo e o endereço do host.

        Args:
            model_name (str): O nome do modelo Ollama a ser usado (ex: "llama3.2").
            host (str): O endereço do servidor Ollama.
        """
        self.model_name = model_name
        self.url = f"{host}/api/generate"
        self.prompt_template = """Você é um assistente de IA projetado para ajudar estudantes da Universidade de Brasília a encontrar turmas. Sua tarefa é identificar e recuperar as turmas mais relevantes e *únicas* da base de conhecimento, com base no conteúdo da disciplina que o usuário está procurando. Desconsidere quaisquer palavras, frases ou elementos conversacionais na entrada do usuário que não contribuam para a identificação do tema da disciplina. Sua busca deve ser altamente precisa, utilizando o termo ou a frase extraída para encontrar correspondências relevantes em todos os detalhes da turma, incluindo a ementa, o nome da disciplina e o nome do componente. Retorne os detalhes completos das turmas mais relevantes e únicas, incluindo:

- Disciplina: [Nome da Disciplina]
- Unidade responsável: [Unidade responsável]
- Ementa: [Ementa da disciplina]

Apresente os resultados como uma lista ranqueada.

Aqui está a base de conhecimento:

{{ knowledge {Retrieval:FortyMoonsPick} }}

A consulta do usuário é:
"""

    def get_turmas_info(self, user_query: str):
        """
        Envia a consulta do usuário para o modelo Ollama e retorna a resposta.

        Args:
            user_query (str): A pergunta do usuário sobre as turmas.

        Returns:
            str: A resposta gerada pelo modelo.
        """
        # O fluxo RAG do seu agente já lida com o retrieval.
        # Aqui, apenas formatamos o prompt final para o passo de geração.
        # O template {{knowledge...}} é processado pela sua ferramenta de fluxo.
        # O que enviamos para o Ollama é a consulta do usuário dentro do prompt.
        full_prompt = f"{self.prompt_template}\n{user_query}"

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload, timeout=120) # Timeout de 120s
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Nenhuma resposta recebida do modelo.").strip()
        except requests.Timeout:
            return "Erro: A requisição demorou muito para responder (timeout)."
        except requests.RequestException as e:
            return f"Erro ao conectar com o Ollama: {e}"