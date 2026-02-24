def build_structured_shap(shap_features):
    if not shap_features:
        return {
            "top_positive": [],
            "top_negative": [],
            "vector_available": False
        }

    pos = []
    neg = []

    for f, v in shap_features.items():
        if isinstance(v, list):
            v = v[0]

        v = float(v)

        if v > 0:
            pos.append({"feature": f, "impact": round(v, 3)})
        else:
            neg.append({"feature": f, "impact": round(v, 3)})

    pos = sorted(pos, key=lambda x: abs(x["impact"]), reverse=True)[:3]
    neg = sorted(neg, key=lambda x: abs(x["impact"]), reverse=True)[:3]

    return {
        "top_positive": pos,
        "top_negative": neg,
        "vector_available": True
    }  