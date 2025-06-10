# app.py
import streamlit as st
from ragflow_client import RagflowClient

# --- Configuração da Página ---
st.set_page_config(
    page_title="Assistente de Turmas UnB",
    page_icon="📚",
    layout="centered"
)

# --- Título e Descrição ---
st.title("📚 Assistente de Turmas da UnB")
st.write("Converse com o assistente oficial para encontrar informações sobre disciplinas.")

# --- Inicialização do Cliente ---
@st.cache_resource
def get_ragflow_client():
    return RagflowClient()

client = get_ragflow_client()

# --- Gerenciamento do Histórico de Mensagens ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico da conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input do Usuário ---
if prompt := st.chat_input("Qual o tema da disciplina que você procura?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando na base de conhecimento..."):
            # A chamada ao cliente agora é mais simples, sem passar o chat_id
            response = client.get_completion(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})