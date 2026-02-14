from services1.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c

def generate_reasoning(input_data: dict):
    # Step 1 — get ML prediction
    pred = predict_patient(input_data)
    risk_score = pred["risk_score"]

    # Step 2 — run stage-4c orchestration
    reasoning = run_stage_4c(input_data, risk_score)

    return reasoning
