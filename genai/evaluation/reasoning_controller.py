

def compute_reasoning_confidence(risk_score: float,shap_available: float, retrieval_count: int) -> float:
    certainty = abs(risk_score - 0.5) * 2

    shap_signal = 1 if structured_shap.get("vector_available",False) else 0
    retrieval_signal = 1 if retrieval_count > 0 else 0

    confidence = 0.7 * certainty + 0.15 * shap_signal + 0.15 * retrieval_signal
    if 0.45 <=risk_score <=0.55:
        confidence *=0.9

    if shap_signal == 0 and retrieval_signal == 0:
        confidence *= 0.92
    return round(confidence, 3)

def decide_mode(confidence: float):
    if confidence < 0.30:
        return "SAFE"
    elif confidence < 0.65:
        return "VERBOSE"
    else:
        return "NORMAL"

def detect_explanation_mismatch(structured_shap, llm_text: str):
    if not structured_shap.get("vector_available") or not llm_text:
        return False

    shap_features = {f["feature"] for f in structured_shap["top_positive"]}

    return not any(f.lower() in llm_text.lower() for f in shap_features)