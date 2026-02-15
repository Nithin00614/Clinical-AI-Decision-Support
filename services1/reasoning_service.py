from services1.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services.hitl_override_service import get_override

def run_reasoning(input_data: dict):

    # Step-1 prediction
    pred = predict_patient(input_data)

    # Step-2 orchestration
    stage4 = run_stage_4c(input_data, pred["risk_score"])

    # Step-3 LLM reasoning
    llm_result = run_llm_stage(stage4)

    override = get_override(input_data.get("patient_id"))

    if override:
        llm_result["decision_mode"] = override["override_decision"]
        llm_result["decision_source"] = "CLINICIAN_OVERRIDE"
    else:
        llm_result["decision_source"] = "MODEL"

    # attach outputs
    llm_result["risk_score"] = pred["risk_score"]

    return {
        **llm_result,
        "decision_mode": llm_result["decision_mode"],
        "decision_source": llm_result["decision_source"]
    }
