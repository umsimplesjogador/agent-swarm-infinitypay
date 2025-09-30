# from app.rag.vectorstore import VectorStore
# from app.llm.gemini_client import ask_gemini
# from typing import Dict

# class KnowledgeAgent:
#     def __init__(self):
#         self.vs = VectorStore()

#     def _format_context(self, hits):
#         s = ""
#         for i, h in enumerate(hits, 1):
#             s += f"[Contexto {i} - fonte: {h['meta']['source']}\n]{h['text']}\n\n"
#         return s

#     def answer(self, query: str) -> Dict:
#         hits = self.vs.query(query, top_k=4)
#         context = self._format_context(hits)
#         prompt = f"""Você é um assistente que responde perguntas sobre a InfinitePay usando somente o contexto fornecido.
# Contexto:
# {context}
# Pergunta: {query}

# Instruções:
# - Responda em Português.
# - Use apenas as informações do contexto; se a informação não estiver no contexto, admita que não sabe e sugira consultar o site.
# - Forneça referência das fontes usadas.
# """
#         text = ask_gemini(prompt, system="Você é um assistente especializado em produtos e serviços da InfinitePay.")
#         sources = list({h['meta']['source'] for h in hits})
#         return {"answer": text, "sources": sources}



from app.rag.vectorstore import VectorStore
from app.llm.gemini_client import ask_gemini
from typing import Dict

class KnowledgeAgent:
    def __init__(self):
        self.vs = VectorStore()

    def _format_context(self, hits):
        s = ""
        for h in hits:
            s += f"{h['text']} (Fonte: {h['meta']['source']})\n\n"
        return s


    def answer(self, query: str) -> Dict:
        # Recupera os trechos relevantes do RAG
        hits = self.vs.query(query, top_k=4)
        context = self._format_context(hits)

        # Prompt refinado
        prompt = f"""Contexto sobre a InfinitePay:
{context}

Pergunta do usuário:
{query}

Instruções:
- Responda em Português de forma clara e detalhada.
- Analise o contexto da pergunta.
- Evite repetir links ou informações desnecessárias.
- Se a informação não estiver no contexto, indique que não sabe e sugira consultar o site.
- Forneça referências das fontes usadas de forma compacta.
"""

        # Instrução de sistema
        system_instruction = (
            "Você é um assistente especializado em produtos e serviços da InfinitePay. "
            "Responda de forma detalhada, completa e natural, usando exemplos quando aplicável."
        )

        # Chamada para Gemini
        text = ask_gemini(prompt, system=system_instruction)

        # Substitui caracteres literais "\n" por quebras de linha reais
        text = text.replace("\\n", "\n").strip()

        # Extrai fontes únicas
        sources = list({h['meta']['source'] for h in hits})

        return {"answer": text, "sources": sources}

