import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
GLOBAL_SHAP_PATH = BASE_DIR / "genai" / "data" / "artifacts" / "global_shap_importance.json"

_global_shap = None

def get_global_shap():
    global _global_shap
    if _global_shap is None:
        with open(GLOBAL_SHAP_PATH, "r") as f:
            _global_shap = json.load(f)
    return _global_shap