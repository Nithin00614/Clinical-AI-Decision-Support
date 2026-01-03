from pathlib import Path
from pypdf import PdfReader

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "guidelines"

def load_pdfs():
    texts = []
    sources = []
    for pdf in DATA_DIR.glob("*.pdf"):
        reader = PdfReader(str(pdf))
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                texts.append(text)
                sources.append(f"{pdf.name}::page_{i+1}")
    return texts, sources

if __name__ == "__main__":
    texts, sources = load_pdfs()
    print(f"Loaded {len(texts)} pages")

from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_texts(texts, sources, chunk_size=800, chunk_overlap=120):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = []
    metadatas = []
    for text, src in zip(texts, sources):
        splits = splitter.split_text(text)
        for s in splits:
            chunks.append(s)
            metadatas.append({"source": src})
    return chunks, metadatas

if __name__ == "__main__":
    texts, sources = load_pdfs()
    chunks, metas = chunk_texts(texts, sources)
    print(f"Created {len(chunks)} chunks")
