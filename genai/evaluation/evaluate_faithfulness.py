def evaluate_faithfulness(shap_features, retrieved_chunks):
    """
    shap_features: dict {feature: contribution}
    retrieved_chunks: list of (text, metadata)
    """

    results = {}
    combined_text = " ".join([text.lower() for text, _ in retrieved_chunks])

    for feature in shap_features.keys():
        feature_present = feature.lower() in combined_text
        results[feature] = {
            "supported_by_evidence": feature_present
        }

    return results
