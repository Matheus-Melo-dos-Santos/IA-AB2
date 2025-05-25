import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def responder_pergunta(pergunta, contexto):
    prompt = f"""
    Você é um assistente inteligente. Baseado no conteúdo abaixo, responda à pergunta do usuário.

    CONTEÚDO:
    {contexto[:3000]}

    PERGUNTA:
    {pergunta}

    Responda de forma clara e direta.
    """

    resposta = model.generate_content(prompt)
    return resposta.text.strip()