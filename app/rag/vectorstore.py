from .ingest import RAGIngest, MODEL_NAME
from sentence_transformers import SentenceTransformer
import os

ing = RAGIngest()
MODEL = SentenceTransformer(MODEL_NAME)

class VectorStore:
    def __init__(self):
        self.data = ing.load_index()
        if self.data is None:
            print("Índice não encontrado. Construindo...")
            ing.build_index()
            self.data = ing.load_index()
        self.index = self.data["index"]
        self.docs = self.data["meta"]["docs"]
        self.metas = self.data["meta"]["metas"]

    def query(self, text, top_k=5):
        emb = MODEL.encode([text], convert_to_numpy=True)
        D, I = self.index.search(emb, top_k)
        results = []
        for idx in I[0]:
            results.append({"text": self.docs[idx], "meta": self.metas[idx]})
        return results
