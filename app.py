import streamlit as st
from ragflow_agent_client import RagflowClient
from visualizaJson import processar_json_disciplinas
#from agent_api.config import AGENT_EXPLANATOR_ID

st.set_page_config(page_title="Assistente de Turmas UnB", layout="centered")
st.title("📚 Assistente de Turmas da UnB")
st.header("One", divider=True)
st.subheader("Two", divider=True)
st.markdown("*Streamlit* is **really** ***cool***.")
materia = st.text_area("Digite o conteudo:", height=300)
#Printando MATERIA DIGITADA
print(f'materia digitada : {materia}')

# Inicializa variáveis de estado
if "resposta_agente" not in st.session_state:
    st.session_state.resposta_agente = None
#if "mostrar_detalhes" not in st.session_state:
    #st.session_state.mostrar_detalhes = False
#if "detalhes_agente" not in st.session_state:
    #st.session_state.detalhes_agente = None

if st.button("Analisar"):
    if not materia.strip():
        st.warning("Por favor, cole uma matéria para análise.")
    else:
        with st.spinner("Analisando..."):
            try:
                client = RagflowClient()
                session_id = client.start_session(materia)
                result = client.analyze_materia(materia, session_id)

                if result.get("code") == 0:
                    #resposta = result["data"]["answer"]
                    resposta = processar_json_disciplinas(result)
                    #print(f'RESULT FORMATADO : {resposta}\n')
                    st.session_state.resposta_agente = resposta
                    print(f'Sessio State Resposta:  {st.session_state.resposta_agente}')
                    #st.session_state.detalhes_agente = None  # Limpa caso nova análise
                    #st.session_state.mostrar_detalhes = "FAKE" in resposta.upper()

                    st.success("Resposta do agente:")
                    st.write(resposta)
                else:
                    st.error(f"Erro da API: {result.get('message')}")

            except Exception as e:
                st.error(f"Erro ao conectar com o agente: {e}")