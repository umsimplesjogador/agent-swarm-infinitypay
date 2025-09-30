from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.support_agent import SupportAgent
from typing import Dict, Any

class RouterAgent:
    def __init__(self):
        self.knowledge = KnowledgeAgent()
        self.support = SupportAgent()

    def _intention(self, message: str) -> str:
        msg = message.lower()
        if any(k in msg for k in ["maquininha", "taxa", "tarifa", "rendimento", "pix", "boleto", "receba", "preço", "custo", "valor"]):
            return "knowledge"
        if any(k in msg for k in ["não consigo", "can't", "cant", "erro", "login", "entrar", "senha", "transferir", "transferência"]):
            return "support"
        if any(k in msg for k in ["quando", "qual", "como", "what", "when", "how", "why"]):
            return "knowledge"
        return "knowledge"

    def handle(self, message: str, user_id: str) -> Dict[str, Any]:
        intent = self._intention(message)
        if intent == "knowledge":
            resp = self.knowledge.answer(message)
            return {"reply": resp["answer"], "agent": "knowledge", "sources": resp.get("sources", []), "meta": {"intent": intent}}
        elif intent == "support":
            resp = self.support.handle_support(message, user_id)
            return {"reply": resp["answer"], "agent": "support", "sources": resp.get("sources", []), "meta": {"intent": intent}}
        else:
            resp = self.knowledge.answer(message)
            return {"reply": resp["answer"], "agent": "knowledge", "sources": resp.get("sources", []), "meta": {"intent": intent}}
