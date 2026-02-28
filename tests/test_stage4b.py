from genai.evaluation.ablation_tests import run_ablation

risk_score = 0.81
shap_features = {
    "serum_creatinine": 0.32,
    "hemoglobin": 0.21
}

retrieved_chunks = [
    ("Elevated serum creatinine reflects reduced GFR.", 
     {"source": "kdigo_ckd.pdf:page_12"})
]

for mode in ["ml_only", "ml_shap", "full_system"]:
    result = run_ablation(
        mode,
        risk_score,
        shap_features,
        retrieved_chunks
    )
    print(result)
