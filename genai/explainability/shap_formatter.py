from genai.explainability.clinical_shap_translator import translate_shap

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
            pos.append({
                "feature": translate_shap(f),
                "impact": round(v, 3)
            })
        elif v < 0:
            neg.append({
                "feature": translate_shap(f),
                "impact": round(v, 3)
            })

    pos = sorted(pos, key=lambda x: abs(x["impact"]), reverse=True)[:3]
    neg = sorted(neg, key=lambda x: abs(x["impact"]), reverse=True)[:3]

    clean_vals = []

    for v in shap_features.values():
        try:
            if isinstance(v, list):
                v = v[0]
            v = float(v)
            clean_vals.append(abs(v))
        except:
            continue

    vector_available = any(v > 1e-6 for v in clean_vals)

    return {
        "top_positive": pos,
        "top_negative": neg,
        "vector_available": vector_available
    }  