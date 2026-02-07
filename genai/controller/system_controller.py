def decide_mode(payload: dict) -> str:
    confidence = payload.get("confidence", 0.0)
    evidence = payload.get("retrieved_evidence", "")

    if confidence < 0.5 or not evidence.strip():
        return "safe"

    if confidence < 0.75:
        return "restricted"

    return "normal"
