from services1.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage

def run_reasoning(input_data: dict):

    # Step-1 prediction
    pred = predict_patient(input_data)

    # Step-2 orchestration
    stage4 = run_stage_4c(input_data, pred["risk_score"])

    # Step-3 LLM reasoning
    llm_result = run_llm_stage(stage4)

    # attach outputs
    llm_result["risk_score"] = pred["risk_score"]

    return llm_result
