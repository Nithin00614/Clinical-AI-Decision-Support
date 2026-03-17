import pandas as pd
import joblib
import shap
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "full_pipeline.pkl"
BACKGROUND_PATH = BASE_DIR / "genai" / "data" / "artifacts" / "background_sample.csv"


# Load pipeline
# Handle calibrated vs non-calibrated pipeline


pipeline = joblib.load(MODEL_PATH)

#  unwrap calibrated model safely
if hasattr(pipeline, "calibrated_classifiers_"):
    base_pipeline = pipeline.calibrated_classifiers_[0].estimator
else:
    base_pipeline = pipeline

preprocessor = base_pipeline.named_steps["preprocessor"]
model = base_pipeline.named_steps["model"]


# Lazy globals
_background_transformed = None
_explainer = None
_feature_names = None


def load_expected_features():
    path = Path("artifacts/expected_features.json")
    if path.exists():
        return set(json.loads(path.read_text()))
    return set()


# Lazy background transform
def get_background():
    global _background_transformed

    if _background_transformed is None:
        try:
            background_df = pd.read_csv(BACKGROUND_PATH)
            _background_transformed = preprocessor.transform(background_df)
        except Exception as e:
            logger.warning(f"Failed loading SHAP background: {e}")
            _background_transformed = None

    return _background_transformed


# Lazy explainer
def get_explainer():
    global _explainer

    if _explainer is None:
        background = get_background()
        if background is None:
            return None

        try:
            _explainer = shap.Explainer(model, background)
        except Exception as e:
            logger.warning(f"SHAP explainer creation failed: {e}")
            _explainer = None

    return _explainer



# Lazy feature names
def get_feature_names():
    global _feature_names

    if _feature_names is None:
        try:
            _feature_names = preprocessor.get_feature_names_out()
        except Exception as e:
            logger.warning(f"Feature name extraction failed: {e}")
            _feature_names = None

    return _feature_names



# Instance explanation
def explain_instance(df: pd.DataFrame):
    try:
        explainer = get_explainer()
        feature_names = get_feature_names()

        if explainer is None or feature_names is None:
            return None, None

        # ALWAYS create X before any checks
        X = preprocessor.transform(df)

        background = get_background()
        if background is None:
            logger.warning("SHAP skipped — background unavailable")
            return None, None

        if X.shape[1] != background.shape[1]:
            logger.warning(
                f"SHAP skipped — feature mismatch instance={X.shape[1]} background={background.shape[1]}"
            )
            return None, None

        shap_values = explainer(X)[0]

        return shap_values.values, feature_names

    except Exception as e:
        logger.warning(f"SHAP explanation failed: {e}")
        return None, None