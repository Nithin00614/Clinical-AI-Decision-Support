def evaluate_grounding(retrieved_chunks):
    """
    retrieved_chunks: list of (text, metadata)
    """

    if not retrieved_chunks or len(retrieved_chunks) == 0:
        return {
            "grounded": False,
            "reason": "No guideline evidence retrieved"
        }

    return {
        "grounded": True,
        "num_evidence_chunks": len(retrieved_chunks)
    }
