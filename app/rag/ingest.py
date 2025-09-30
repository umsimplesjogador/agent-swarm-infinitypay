import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import os, pickle

MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
SOURCE_URLS = [
    "https://www.infinitepay.io",
    "https://www.infinitepay.io/maquininha",
    "https://www.infinitepay.io/maquininha-celular",
    "https://www.infinitepay.io/tap-to-pay",
    "https://www.infinitepay.io/pdv",
    "https://www.infinitepay.io/receba-na-hora",
    "https://www.infinitepay.io/gestao-de-cobranca",
    "https://www.infinitepay.io/gestao-de-cobranca-2",
    "https://www.infinitepay.io/link-de-pagamento",
    "https://www.infinitepay.io/loja-online",
    "https://www.infinitepay.io/boleto",
    "https://www.infinitepay.io/conta-digital",
    "https://www.infinitepay.io/conta-pj",
    "https://www.infinitepay.io/pix",
    "https://www.infinitepay.io/pix-parcelado",
    "https://www.infinitepay.io/emprestimo",
    "https://www.infinitepay.io/cartao",
    "https://www.infinitepay.io/rendimento",
]

INDEX_DIR = os.getenv("INDEX_DIR", "/data/index")
os.makedirs(INDEX_DIR, exist_ok=True)

class RAGIngest:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.index_path = os.path.join(INDEX_DIR, "faiss_idx.bin")
        self.meta_path = os.path.join(INDEX_DIR, "meta.pkl")

    def _scrape_text(self, url: str) -> str:
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for s in soup(["script", "style", "noscript"]):
                s.decompose()
            texts = [t.get_text(separator=" ", strip=True) for t in soup.find_all(["p","h1","h2","h3","li"])]
            return "\n".join([t for t in texts if t])
        except Exception as e:
            print(f"[scrape] erro {url}: {e}")
            return ""

    def build_index(self, urls=SOURCE_URLS):
        docs, metas = [], []
        for url in urls:
            text = self._scrape_text(url)
            if not text:
                continue
            parts = [p.strip() for p in text.split("\n") if p.strip()]
            for p in parts:
                if len(p) < 50:
                    continue
                docs.append(p)
                metas.append({"source": url})
        if not docs:
            raise RuntimeError("Nenhum documento coletado para indexar.")
        embeddings = self.model.encode(docs, show_progress_bar=True, convert_to_numpy=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        faiss.write_index(index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump({"docs": docs, "metas": metas}, f)
        return {"count": len(docs)}

    def load_index(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.meta_path):
            return None
        index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            meta = pickle.load(f)
        return {"index": index, "meta": meta}
