from services.inference_service import predict_patient
from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services.hitl_override_service import get_override
from genai.guardrails.feature_aliignment_guardrail import validate_feature_alignment
from genai.evaluation.traceability import compute_driver_evidence_traceability
from genai.evaluation.explanation_coverage import compute_explanation_coverage
from genai.evaluation.reliability_score import compute_explanation_reliability
import logging
import time
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinical-ai")

def run_reasoning(input_data: dict):

    pipeline_start = time.time()
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

    full_exp = (
    llm_result.get("full_explanation")
    or llm_result.get("explanation")
    or llm_result.get("analysis")
    or llm_result.get("text")
    )

    explanation = full_exp or ""

    drivers_list = stage4.get("drivers_list", [])

    # Use raw evidence chunks for reliability computation
    evidence = stage4.get("_evidence_chunks", [])

    traceability = compute_driver_evidence_traceability(drivers_list, evidence)

    coverage = compute_explanation_coverage(explanation, drivers_list)

    reliability_score, reliability_label = compute_explanation_reliability(
        traceability,
        coverage
    )

    # Attach LLM reasoning outputs

    llm_result["explanation_reliability"] = {
    "score": round(reliability_score, 3),
    "level": reliability_label,
    "traceability": traceability,
    "coverage": coverage
    }

    if reliability_label == "LOW":
        llm_result["decision_mode"] = "SAFE"

    aligned, offending = validate_feature_alignment(full_exp, drivers_list)

    if not aligned:
        llm_result["decision_mode"] = "SAFE"
        llm_result["reasoning_validation"] = {
            "aligned": False,
            "offending_term": offending
        }
    else:
        llm_result["reasoning_validation"] = {
            "aligned": True
        }

    # handle structured guardrail output
    if isinstance(full_exp, dict):
        full_exp = full_exp.get("full_text") or full_exp.get("text")

    reasoning = {
        "clinician_summary": llm_result.get("clinician_summary", ""),
        "full_explanation": full_exp or "",
        "references": llm_result.get("references", [])
    }
    

    override = get_override(input_data.get("patient_id"))

    if override:
        llm_result["decision_mode"] = override["override_decision"]
        llm_result["decision_source"] = "CLINICIAN_OVERRIDE"
        stage4["confidence"] = round(stage4["confidence"] * 0.75, 3)
    else:
        llm_result["decision_source"] = "MODEL"

    audit_entry = {
    "patient_id": input_data.get("patient_id"),
    "risk_score": stage4.get("risk_score"),
    "confidence": stage4.get("confidence"),
    "decision_mode": llm_result.get("decision_mode"),
    "explanation_reliability": llm_result.get("explanation_reliability"),
    "traceability": llm_result.get("explanation_reliability", {}).get("traceability"),
    "coverage": llm_result.get("explanation_reliability", {}).get("coverage"),
    "timestamp": time.time()
}

    with open("hitl_audit_log.jsonl", "a") as f:
        f.write(json.dumps(audit_entry) + "\n")    

    # attach outputs
    llm_result["risk_score"] = stage4["risk_score"]
    llm_result["confidence"] = stage4["confidence"]
    llm_result["decision_mode"] = stage4["decision_mode"]
    llm_result["explainabilty_status"] = llm_result["reasoning_metadata"]["explainability_status"]

    logger.info(
        f"{input_data.get('patient_id')} | "
        f"risk={stage4['risk_score']:.3f} | "
        f"conf={stage4['confidence']:.3f} | "
        f"mode={stage4['decision_mode']}"
    )

    total_latency_ms = (time.time() - pipeline_start) * 1000

    return {
    "prediction": {
        "risk_score": stage4["risk_score"],
        "confidence": stage4["confidence"],
        "decision_mode": stage4["decision_mode"],
        "decision_source": llm_result["decision_source"],
        "model_version": stage4.get("model_version", "UNKNOWN")
    },

    "explainability": {
        "shap": stage4.get("shap"),
        "shap_available": stage4.get("shap_available", False),
        "shap_explanation": llm_result.get("shap_explanation"),
        "explainability_status": llm_result.get("explainability_status"),
    },

    "retrieval": {
        "used": bool(stage4.get("retrieved_evidence")),
        "evidence": stage4.get("retrieved_evidence") or [],
    },

    "reasoning": {
        "clinician_summary": reasoning["clinician_summary"],
        "full_explanation": reasoning["full_explanation"],
        "references": reasoning.get("references", []),
        "metadata": llm_result.get("reasoning_metadata", {}),
        "explanation_reliability": llm_result.get("explanation_reliability", {}),
    },

    "system_metrics": {
    "retrieval_latency_ms": stage4.get("retrieval_latency_ms", 0.0),
    "shap_latency_ms": stage4.get("shap_latency_ms"),
    "llm_latency_ms": llm_result.get("llm_latency_ms",0.0),
    "total_latency_ms": round(total_latency_ms, 2)
}
}