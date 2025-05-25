import streamlit as st
from decisor import avaliar_candidato
from explicador_llm import gerar_justificativa

st.title("Sistema de Seleção de Candidatos")

# Entrada do usuário
nome_candidato = st.text_input("Nome do Candidato")
vaga = "Analista de Dados" # A vaga agora é fixa
experiencia = st.slider("Anos de experiência", 0, 10, 2)
formacao = st.text_input("Formação (ex: Ciência da Computação)")
habilidades = st.text_area("Habilidades (ex: Python, SQL, Liderança)")

if st.button("Avaliar Candidato"):
    dados = {
        "nome_candidato": nome_candidato,
        "vaga": vaga,
        "experiencia": experiencia,
        "formacao": formacao,
        "habilidades": habilidades
    }

    decisao = avaliar_candidato(dados)
    st.markdown(f"**Resultado para {nome_candidato}:** {decisao}")

    justificativa = gerar_justificativa(dados, decisao)
    st.markdown("**Justificativa (Equipe RH):**")
    st.write(justificativa)