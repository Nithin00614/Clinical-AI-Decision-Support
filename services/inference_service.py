import pandas as pd
import joblib
from pathlib import Path
from genai.explainability.shap_loader import explain_instance
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
import logging

# Load trained pipeline
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "full_pipeline.pkl"

pipeline = joblib.load(MODEL_PATH)

#  unwrap calibrated model safely
if hasattr(pipeline, "calibrated_classifiers_"):
    base_pipeline = pipeline.calibrated_classifiers_[0].estimator
else:
    base_pipeline = pipeline

preprocessor = base_pipeline.named_steps["preprocessor"]
model = base_pipeline.named_steps["model"]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinical-ai")

def predict_patient(input_data: dict):

    FEATURE_MAP = {
        "bp": "Bp",
        "sg": "Sg",
        "al": "Al",
        "su": "Su",
        "rbc": "Rbc",
        "bu": "Bu",
        "sc": "Sc",
        "sod": "Sod",
        "pot": "Pot",
        "hemo": "Hemo",
        "wbcc": "Wbcc",
        "rbcc": "Rbcc",
        "htn": "Htn"
    }

    mapped_input = {FEATURE_MAP[k]: v for k, v in input_data.items()}
    df = pd.DataFrame([mapped_input])

    shap_values, feature_names = explain_instance(df)

    if shap_values is not None:
        shap_features = dict(
            sorted(zip(feature_names, shap_values),
                key=lambda x: abs(x[1]),
                reverse=True)[:5]
        )
    else:
        shap_features = {}
    logger.info(f"SHAP generated: {bool(shap_features)}")
    bp = base_pipeline.predict_proba
    risk_score = float(pipeline.predict_proba(df)[0][1])
    shap_features = shap_features


    return {
        "risk_score": risk_score,
        "shap_features": shap_features
    }
