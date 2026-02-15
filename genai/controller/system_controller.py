def decide_mode(payload):

    confidence = payload.get("confidence", 1.0)
    risk = payload.get("risk_score", 0.5)

    # SAFE when uncertainty high
    if risk >= 0.85 or confidence < 0.50:
        return "SAFE"

    # VERBOSE when medium confidence OR borderline risk
    if 0.40 <= risk < 0.85:
        return "VERBOSE"

    return "NORMAL"

