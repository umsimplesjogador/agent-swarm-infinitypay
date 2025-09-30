# import os
# import google.generativeai as genai

# api_key = os.getenv("GEMINI_API_KEY")

# def ask_gemini(prompt: str) -> str:
#     if not api_key:
#         return "[OFFLINE] GEMINI_API_KEY não configurada."
#     genai.configure(api_key=api_key)
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt)
#     return response.text



import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega o .env do mesmo diretório do script
env_path = os.path.join(os.path.dirname(__file__), "GEMINI_API_KEY.env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt: str, system: str = None) -> str:
    """
    Envia prompt para o modelo Gemini e retorna texto gerado.
    Aceita instrução opcional 'system' que será adicionada ao prompt.
    """
    if not api_key:
        return "[OFFLINE] GEMINI_API_KEY não configurada."

    # Adiciona instrução system ao prompt
    if system:
        prompt = f"System: {system}\nUser: {prompt}"

    # Configura a API e gera a resposta
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
    response = model.generate_content(prompt)
    return response.text
