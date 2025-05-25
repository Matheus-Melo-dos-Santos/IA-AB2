import streamlit as st
from pdf_loader import carregar_texto_pdf
from rag_engine import responder_pergunta

st.title("Agente Conversacional com PDF (RAG + LLM)")

uploaded_file = st.file_uploader("Envie um arquivo PDF", type=["pdf"])

if uploaded_file:
    texto = carregar_texto_pdf(uploaded_file)
    st.session_state["contexto"] = texto
    st.success("PDF carregado com sucesso!")

if "contexto" in st.session_state:
    pergunta = st.text_input("Digite sua pergunta sobre o conteúdo do PDF:")
    if pergunta:
        resposta = responder_pergunta(pergunta, st.session_state["contexto"])
        st.markdown("**Resposta:**")
        st.write(resposta)