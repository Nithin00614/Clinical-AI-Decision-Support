from genai.retrieval.retriever import search

if __name__ == "__main__":
    query = "elevated serum creatinine and chronic kidney disease"
    results = search(query, k=3)

    print("\nTop retrieved chunks:\n")
    for text, meta in results:
        print(meta)
        print(text[:300])
        print("-" * 80)
