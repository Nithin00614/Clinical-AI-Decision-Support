def assign_confidence(
    risk_score: float,
    shap_features: dict,
    retrieved_chunks: list
) -> dict:
    """
    Lightweight confidence estimation for clinical explanations
    """

    shap_strength = sum(abs(v) for v in shap_features.values())
    evidence_count = len(retrieved_chunks)

    if shap_strength > 1.5 and evidence_count >= 3:
        level = "High"
        note = "Multiple contributing features supported by guideline evidence."
    elif shap_strength > 0.8 and evidence_count >= 1:
        level = "Moderate"
        note = "Partial feature support with limited guideline evidence."
    else:
        level = "Low"
        note = "Insufficient evidence or weak feature attribution."

    return {
        "confidence_level": level,
        "confidence_note": note
    }
