# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from app.agents.router import RouterAgent

# app = FastAPI(title="Agent Swarm - CloudWalk Case (Infinitepay)")

# class RequestPayload(BaseModel):
#     message: str
#     user_id: str

# router = RouterAgent()

# @app.post("/process")
# async def process(payload: RequestPayload):
#     try:
#         result = router.handle(payload.message, payload.user_id)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/health")
# def health():
#     return {"status": "ok"}



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from app.agents.router import RouterAgent
# import os

# app = FastAPI(title="Agent Swarm - CloudWalk Case (Infinitepay)")

# # --- Payload do endpoint /process ---
# class RequestPayload(BaseModel):
#     message: str
#     user_id: str

# # --- Inicializa o router (carrega vectorstore de forma preguiçosa) ---
# router = RouterAgent()

# # --- Endpoint raiz para teste ---
# @app.get("/")
# def root():
#     return {"message": "Agent Swarm API Rodando!"}

# # --- Endpoint de health check ---
# @app.get("/health")
# def health():
#     return {"status": "ok"}

# # --- Endpoint principal de processamento ---
# @app.post("/process")
# async def process(payload: RequestPayload):
#     try:
#         result = router.handle(payload.message, payload.user_id)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents.router import RouterAgent
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Agent Swarm - CloudWalk Case (Infinitepay)")

# --- Payload do endpoint /process ---
class RequestPayload(BaseModel):
    message: str
    user_id: str

# --- Inicializa o router (carrega vectorstore de forma preguiçosa) ---
router = RouterAgent()

# --- Armazena histórico simples em memória ---
conversation_history: Dict[str, List[Dict[str, str]]] = {}

# --- Endpoint raiz ---
@app.get("/")
def root():
    return {"message": "Agent Swarm API Rodando!"}

# --- Health check ---
@app.get("/health")
def health():
    return {"status": "ok"}

# Caminho da pasta onde está o index.html
app_root = os.path.dirname(os.path.abspath(__file__))

# Serve arquivos estáticos
app.mount("/static", StaticFiles(directory=app_root), name="static")

@app.get("/chat")
def chat():
    return FileResponse(os.path.join(app_root, "index.html"))


# --- Endpoint de processamento com histórico ---
@app.post("/process")
async def process(payload: RequestPayload):
    try:
        user_id = payload.user_id
        message = payload.message

        # Inicializa histórico se não existir
        if user_id not in conversation_history:
            conversation_history[user_id] = []

        # Adiciona a mensagem do usuário ao histórico
        conversation_history[user_id].append({"role": "user", "message": message})

        # Chama o RouterAgent para gerar resposta
        agent_response = router.handle(message, user_id)

        # Extrai apenas o texto da resposta
        reply_text = agent_response.get("reply") or agent_response.get("answer") or str(agent_response)

        # Adiciona resposta do agente ao histórico
        conversation_history[user_id].append({"role": "agent", "message": reply_text})

        # Retorna texto limpo + histórico
        return {
            "response": reply_text,
            "sources": agent_response.get("sources", []),
            "meta": agent_response.get("meta", {}),
            "history": conversation_history[user_id]
        }

    except Exception as e:
        print("ERRO no /process:", e)
        raise HTTPException(status_code=500, detail=str(e))

