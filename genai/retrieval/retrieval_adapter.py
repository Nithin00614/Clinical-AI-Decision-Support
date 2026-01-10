def format_retrieved_chunks(results, max_chunks=4):
    formatted = []
    for text, meta in results[:max_chunks]:
        source = meta.get("source", "unknown")
        formatted.append(f"[{source}]\n{text.strip()}")
    return "\n\n".join(formatted)
