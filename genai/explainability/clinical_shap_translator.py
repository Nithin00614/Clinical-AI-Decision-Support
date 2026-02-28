 
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


def normalize(x: str):
    return (
        str(x)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def translate_shap(name: str) -> str:
    if not name:
        return name

    norm_name = normalize(name)

    for k, v in FEATURE_NAME_MAP.items():
        if normalize(k) == norm_name:
            return v

    return name

def generate_clinical_sentences(structured_shap: dict):
    if not structured_shap or not structured_shap.get("vector_available"):
        return []

    drivers = []

    for f in structured_shap.get("top_positive", []):
        drivers.append((f["feature"]))

    for f in structured_shap.get("top_negative", []):
        drivers.append((f["feature"]))

    # remove duplicates while preserving order
    seen = set()
    drivers = [x for x in drivers if not (x in seen or seen.add(x))]

    return drivers