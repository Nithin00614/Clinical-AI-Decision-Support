import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent

# Load index
index = faiss.read_index(str(BASE_DIR / "ckd_guidelines.index"))

# Load chunks + metadata
with open(BASE_DIR / "chunks.pkl", "rb") as f:
    store = pickle.load(f)

chunks = store["chunks"]
metas = store["metas"]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, k=5):
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(q_emb, k)
    results = []
    for idx in I[0]:
        results.append((chunks[idx], metas[idx]))
    return results

if __name__ == "__main__":
    query = "elevated serum creatinine and chronic kidney disease"
    results = search(query, k=3)

    print("\nTop retrieved chunks:\n")
    for text, meta in results:
        print(meta)
        print(text[:300], "\n", "-" * 80)
