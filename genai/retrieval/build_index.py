from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from genai.ingestion.load_and_chunk import load_pdfs, chunk_texts

INDEX_DIR = Path(__file__).resolve().parents[1] / "retrieval"
INDEX_DIR.mkdir(exist_ok=True)

def build_faiss(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, show_progress_bar=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine via normalized vectors
    index.add(embeddings)
    return index, model

if __name__ == "__main__":
    texts, sources = load_pdfs()
    chunks, metas = chunk_texts(texts, sources)

    index, model = build_faiss(chunks)

    faiss.write_index(index, str(INDEX_DIR / "ckd_guidelines.index"))
    with open(INDEX_DIR / "chunks.pkl", "wb") as f:
        pickle.dump({"chunks": chunks, "metas": metas}, f)

    print("Index and chunks saved.")
