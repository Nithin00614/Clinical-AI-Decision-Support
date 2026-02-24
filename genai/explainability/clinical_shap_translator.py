 
FEATURE_NAME_MAP = {
    "num_Hemo": "Hemoglobin",
    "num_Sc": "Serum creatinine",
    "num_Sod": "Sodium",
    "num_Pot": "Potassium",
    "num_Bu": "Blood urea",
    "num_Sg": "Specific gravity",
    "num_Al": "Albumin",
    "num_Su": "Sugar",
    "num_Rbcc": "RBC count",
    "num_Wbcc": "WBC count",
    "bin_Htn": "Hypertension",
    "num_Bp": "Blood pressure",
}


def translate_shap(name: str) -> str:
    return FEATURE_NAME_MAP.get(name, name)


def generate_clinical_sentences(structured_shap: dict):
    if not structured_shap or not structured_shap.get("vector_available"):
        return []

    sentences = []

    for f in structured_shap["top_positive"]:
        feature = translate_shap(f["feature"])
        sentences.append(f"{feature} increased CKD risk")

    for f in structured_shap["top_negative"]:
        feature = translate_shap(f["feature"])
        sentences.append(f"{feature} reduced CKD risk")

    return sentences