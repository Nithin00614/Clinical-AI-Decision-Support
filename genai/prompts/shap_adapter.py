def format_shap_features(shap_dict, top_k=5):

    friendly = {
        "hemo": "Hemoglobin",
        "sg": "Specific gravity",
        "rbcc": "Red blood cell count",
        "su": "Serum urea",
        "bp": "Blood pressure",
        "sc": "Serum creatinine",
        "htn": "Hypertension"
    }

    sorted_items = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    lines = []

    for feature, value in sorted_items[:top_k]:
        name = friendly.get(feature, feature)
        direction = "increased CKD risk" if value > 0 else "reduced CKD risk"
        lines.append(f"• {name} {direction}")

    return "\n".join(lines)