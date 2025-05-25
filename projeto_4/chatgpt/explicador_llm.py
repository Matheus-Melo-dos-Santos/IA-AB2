import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gerar_justificativa(dados, decisao):
    nome_candidato = dados.get("nome_candidato", "o candidato")
    vaga = dados.get("vaga", "uma vaga")
    experiencia = dados.get("experiencia", 0)
    formacao = dados.get("formacao", "").lower()
    habilidades = dados.get("habilidades", "").lower()

    prompt = f"""
    Você é um especialista em RH. A Equipe RH avaliou o(a) candidato(a) {nome_candidato} para a vaga de {vaga}.
    Com base nas seguintes informações:
    - Experiência: {experiencia} anos
    - Formação: {formacao}
    - Habilidades: {habilidades}

    O(A) candidato(a) foi classificado(a) como '{decisao}'.

    Escreva uma explicação curta e clara para essa decisão, direcionada à Equipe RH.
    """

    model = genai.GenerativeModel('gemini-1.5-flash-001') # Ou o modelo que você identificou como suportado
    response = model.generate_content(prompt)

    return response.text.strip()