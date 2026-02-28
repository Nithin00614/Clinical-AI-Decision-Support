def compute_explanation_confidence(model_conf, vector_available, retrieval_count):
    return round(
        min(1.0,
            0.7 * model_conf +
            0.2 * float(vector_available) +
            0.1 * (1.0 if retrieval_count > 0 else 0.0)
        ),
        3
    )


def compute_explainability_reliability(structured_shap, shap_missing_features, shap_mismatch):
    
    if not structured_shap.get("vector_available"):
        return "LOW"

    if shap_mismatch or len(shap_missing_features) > 0:
        return "MEDIUM"

    return "HIGH"


def compute_reasoning_reliability(model_conf, retrieval_count, vector_available):

    if model_conf < 0.5:
        return "LOW"

    if retrieval_count == 0 or not vector_available:
        return "MEDIUM"

    return "HIGH"    


def compute_clinician_trust(explainability_rel, reasoning_rel):

    if explainability_rel == "HIGH" and reasoning_rel == "HIGH":
        clinician_trust = "HIGH"

    elif explainability_rel == "LOW" or reasoning_rel == "LOW":
        clinician_trust = "LOW"

    else:
        clinician_trust = "MEDIUM"

    return clinician_trust

def calibrate_reasoning_confidence(
    base_conf: float,
    risk_score: float,
    vector_available: bool,
    retrieval_count: int,
):
    """
    Explanation-aware medical confidence calibration
    Prevents unsafe overconfidence in clinical scenarios
    """

    conf = float(base_conf)

    # --- SHAP reliability penalty ---
    if not vector_available:
        conf *= 0.75

    # --- Evidence grounding boost ---
    conf *= min(1.0, 0.85 + 0.05 * retrieval_count)

    # --- High-risk medical overconfidence control ---
    if risk_score > 0.8:
        conf *= 0.93

    # --- Clamp ---
    conf = max(0.0, min(conf, 1.0))

    return round(conf, 3)    