def format_shap_features(shap_dict, top_k=5):
    """
    shap_dict example:
    {
      "sc": 0.42,
      "hemo": -0.31,
      "bp": 0.18
    }
    """
    sorted_items = sorted(
        shap_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    lines = []
    for feature, value in sorted_items[:top_k]:
        direction = "increased" if value > 0 else "decreased"
        lines.append(f"- {feature}: {direction} risk contribution")

    return "\n".join(lines)
