# check_connection.py
print("--- Iniciando teste de conexão direta com RAGflow ---")

try:
    # Importa as variáveis de ambiente para verificação
    from config import RAGFLOW_API_KEY, RAGFLOW_BASE_URL, RAGFLOW_DIALOGUE_ID

    if not RAGFLOW_API_KEY or not RAGFLOW_BASE_URL or not RAGFLOW_DIALOGUE_ID:
        print("\nERRO: Uma ou mais variáveis de ambiente não foram carregadas. Verifique seu arquivo .env")
    else:
        print("OK: Variáveis de ambiente carregadas.")
        # Não imprimimos a chave por segurança
        print(f"-> URL Base: {RAGFLOW_BASE_URL}")
        print(f"-> ID de Diálogo: {RAGFLOW_DIALOGUE_ID}")

    from ragflow_client import RagflowClient
    print("OK: Cliente Ragflow importado.")

    client = RagflowClient()
    print(f"-> Enviando requisição para o endpoint: {client.endpoint_url}")

    # Envia uma consulta de teste
    response = client.get_completion("Este é um simples teste de conexão.")

    print("\n--- RESPOSTA RECEBIDA DO SERVIDOR ---")
    print(response)
    print("-------------------------------------")

except Exception as e:
    print(f"\nERRO INESPERADO: Ocorreu uma exceção durante o teste: {e}")