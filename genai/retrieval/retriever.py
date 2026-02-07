import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# Resolve directory safely
BASE_DIR = Path(__file__).resolve().parent

# Load FAISS index
index = faiss.read_index(str(BASE_DIR / "ckd_guidelines.index"))

# Load chunks + metadata (file is in same directory as this script)
with open(BASE_DIR / "chunks.pkl", "rb") as f:
    store = pickle.load(f)

chunks = store["chunks"]
metas = store["metas"]

# Load embedding model (same as ingestion)
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query: str, k: int = 5):
    """
    Semantic search over CKD guideline chunks.

    Returns:
        List of (text, metadata) tuples
    """
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append((chunks[idx], metas[idx]))

    return results
