import pandas as pd
import joblib
from pathlib import Path

# Load trained pipeline
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "full_pipeline.pkl"

pipeline = joblib.load(MODEL_PATH)

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


    expected = pipeline.feature_names_in_

    for col in expected:
        if col not in df.columns:
            df[col] = 0   # fill missing columns safely

    df = df[expected]
    df = df.reindex(columns=expected, fill_value=0)
    print("INPUT DF:\n", df)
    print("PRED:", pipeline.predict_proba(df))
    print("MODEL LOADED FROM:", MODEL_PATH)
    print("EXPECTED:", pipeline.feature_names_in_)
    print("INPUT:", df.columns.tolist())
    print(pipeline.predict(df))
    print(pipeline.predict_proba(df))
    print(pipeline.named_steps["model"].coef_)


    risk_score = float(pipeline.predict_proba(df)[0][1])

    return {
        "risk_score": risk_score
    }
