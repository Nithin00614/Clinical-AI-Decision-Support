from services.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services.hitl_override_service import get_override
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinical-ai")

def run_reasoning(input_data: dict):

    # Step-1 prediction
    ml_output = predict_patient(input_data)
    logger.info(
    f"ML → risk={ml_output['risk_score']:.3f} | shap={bool(ml_output.get('shap_features'))}"
    )


    if not ml_output.get("shap_features"):
        ml_output["shap_features"] = {}
    
    # Step-2 orchestration
    stage4 = run_stage_4c(input_data=input_data, risk_score=ml_output["risk_score"],shap_features=ml_output.get("shap_features",{}))

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
        stage4["confidence"] = round(stage4["confidence"] * 0.75, 3)
    else:
        llm_result["decision_source"] = "MODEL"

    # attach outputs
    llm_result["risk_score"] = stage4["risk_score"]
    llm_result["confidence"] = stage4["confidence"]
    llm_result["decision_mode"] = stage4["decision_mode"]

    logger.info(
        f"{input_data.get('patient_id')} | "
        f"risk={stage4['risk_score']:.3f} | "
        f"conf={stage4['confidence']:.3f} | "
        f"mode={stage4['decision_mode']}"
    )

    return {
    "prediction": {
        "risk_score": stage4["risk_score"],
        "confidence": stage4["confidence"],
        "decision_mode": stage4["decision_mode"],
        "decision_source": llm_result["decision_source"],
    },
    "explainability": {
        "shap": stage4.get("shap"),
        "shap_explanation": stage4.get("shap_explanation"),
        "retrieved_evidence": stage4.get("retrieved_evidence")
    },
    "reasoning": reasoning
}