def decide_mode(confidence: float, risk_score: float):

    if 0.45 < risk_score <0.55:
        return "SAFE"

    if confidence < 0.30:
        return "SAFE"
    elif confidence < 0.65:
        return "VERBOSE"
    else:
        return "NORMAL"