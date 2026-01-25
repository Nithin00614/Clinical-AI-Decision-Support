import json
from pathlib import Path


def load_shap_artifacts():
    base_dir = Path(__file__).resolve().parents[2]
    shap_path = base_dir / "genai" / "data" / "artifacts" / "shap_output.json"

    with open(shap_path, "r") as f:
        data = json.load(f)

    return data["risk_probability"], data["top_shap_features"]
