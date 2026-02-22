import json
from pathlib import Path


def load_shap_artifacts():
    try:
        base_dir = Path(__file__).resolve().parents[2]
        shap_path = base_dir / "genai" / "data" / "artifacts" / "shap_output.json"

        with open(shap_path, "r") as f:
            data = json.load(f)

        return data.get("top_shap_features", {})

    except Exception as e:
        print("SHAP load failed:", e)
        return {}