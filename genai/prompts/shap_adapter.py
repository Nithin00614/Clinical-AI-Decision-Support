from genai.explainability.clinical_shap_translator import translate_shap


def format_shap_features(shap_dict, top_k=5):

    if not shap_dict:
        return ""

    # sort by absolute importance
    sorted_items = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    lines = []

    for feature, value in sorted_items[:top_k]:

        #  central translation layer
        name = feature

        direction = (
            "increased CKD risk"
            if value > 0
            else "reduced CKD risk"
        )

        lines.append(f"• {name} {direction}")
    return "\n".join(lines)