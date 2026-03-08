import re

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
DRIVER_NORMALIZATION_MAP = {
    "hb": "hemoglobin",
    "hemoglobin": "hemoglobin",

    "rbc": "red blood cell",
    "red blood cell": "red blood cell",
    "red blood cells": "red blood cell",

    "blood pressure": "blood pressure",
    "hypertension": "blood pressure",

    "specific gravity": "specific gravity"
}

DRIVER_SYNONYM_MAP = {

    "blood pressure": [
        "blood pressure",
        "hypertension",
        "bp",
        "hypertensive"
    ],

    "hemoglobin": [
        "hemoglobin",
        "hb",
        "anemia",
        "anemic"
    ],

    "red blood cell": [
        "red blood cell",
        "rbc",
        "erythrocyte"
    ],

    "specific gravity": [
        "specific gravity",
        "urine concentration",
        "urine density"
    ]
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
        drivers.append(f["feature"])

    for f in structured_shap.get("top_negative", []):
        drivers.append(f["feature"])

    # remove duplicates while preserving order
    seen = set()
    drivers = [x for x in drivers if not (x in seen or seen.add(x))]

    return drivers



def extract_driver_features(structured_shap):

    drivers = []

    for item in structured_shap.get("top_positive", []):
        drivers.append(item["feature"])

    for item in structured_shap.get("top_negative", []):
        drivers.append(item["feature"])

    drivers = list(set(drivers))

    driver_map = {
        "blood pressure": ["blood pressure", "hypertension"],
        "hemoglobin": ["hemoglobin", "hb"],
        "rbc count": ["rbc", "red blood cell", "red blood cells"]
    }

    expanded = set()

    for driver in drivers:

        key = driver.lower()

        if key in driver_map:
            expanded.update(driver_map[key])
        else:
            expanded.add(key)

    return list(expanded)


def normalize_drivers(drivers):

    normalized = []

    for d in drivers:
        key = d.lower().strip()

        if key in DRIVER_NORMALIZATION_MAP:
            normalized.append(DRIVER_NORMALIZATION_MAP[key])
        else:
            normalized.append(key)

    return sorted(set(d.lower().strip() for d in normalized))


def filter_evidence_by_shap(evidence_chunks, drivers):

    drivers_norm = []

    for d in drivers:
        key = d.lower().replace("_"," ")

        if key in DRIVER_SYNONYM_MAP:
            drivers_norm.extend(DRIVER_SYNONYM_MAP[key])
        else:
            drivers_norm.append(key)

    filtered = []

    for chunk in evidence_chunks:

        if isinstance(chunk, tuple):
            text = chunk[0]
            chunk_text = chunk[0]
        else:
            text = chunk
            chunk_text = chunk

        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = " ".join(text.split())

        # STRICT SHAP filtering
        if any(driver in text for driver in drivers_norm):
            filtered.append(chunk_text)

    return filtered