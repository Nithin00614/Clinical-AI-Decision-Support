from services1.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services1.hitl_override_service import get_override
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinical-ai")

def run_reasoning(input_data: dict):

    # Step-1 prediction
    pred = predict_patient(input_data)
    print("Pred =", pred)

    # Step-2 orchestration
    stage4 = run_stage_4c(input_data, pred["risk_score"])

    # Step-3 LLM reasoning
    llm_result = run_llm_stage(stage4)

    # Attach LLM reasoning outputs
    
    full_exp = (
    llm_result.get("full_explanation")
    or llm_result.get("explanation")
    or llm_result.get("analysis")
    or llm_result.get("text")
)

    # handle structured guardrail output
    if isinstance(full_exp, dict):
        full_exp = full_exp.get("full_text") or full_exp.get("text")

    reasoning = {
        "clinician_summary": llm_result.get("clinician_summary", ""),
        "full_explanation": full_exp or "",
        "references": llm_result.get("references", "")
    }
    

    override = get_override(input_data.get("patient_id"))

    if override:
        llm_result["decision_mode"] = override["override_decision"]
        llm_result["decision_source"] = "CLINICIAN_OVERRIDE"
    else:
        llm_result["decision_source"] = "MODEL"

    # attach outputs
    llm_result["risk_score"] = stage4["risk_score"]

    logger.info(
        f"{input_data.get('patient_id')} | risk={llm_result['risk_score']} | conf={llm_result.get('confidence')} | mode={llm_result['decision_mode']} | source={llm_result['decision_source']}"
    )

    return {
    "prediction": {
        "risk_score": stage4["risk_score"],
        "confidence": stage4["confidence"],
        "decision_mode": stage4["decision_mode"],
        "decision_source": llm_result["decision_source"],
    },
    "explainability": {
        "shap_explanation": llm_result.get("shap_explanation"),
        "retrieved_evidence": llm_result.get("retrieved_evidence")
    },
    "reasoning": reasoning
}