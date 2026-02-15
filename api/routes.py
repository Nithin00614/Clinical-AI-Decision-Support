import logging
from fastapi import APIRouter, HTTPException
from api.schemas import PatientInput

from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services1.inference_service import predict_patient
from services1.reasoning_service import run_reasoning
from api.schemas_h.hitl_schema import ClinicianReview
import json
from datetime import datetime

logger = logging.getLogger("clinical-ai-api")

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok",
            "service": "clinical-ai-api",
            "version": "v1"
    }


@router.post("/predict")
def predict(input: PatientInput):

    payload = predict_patient(input.dict())

    return payload


@router.post("/reason")
def reasoning_api(payload: PatientInput):
    try:
        result = run_reasoning(payload.dict())

        return {
            "prediction": {
                "risk_score": result.get("risk_score"),
                "confidence": result.get("confidence"),
                "decision_mode": result.get("decision_mode"),
                "decision_source": result.get("decision_source") or "MODEL"
            },
            "explainability": {
                "shap_explanation": result.get("shap_explanation"),
                "retrieved_evidence": result.get("retrieved_evidence"),
            },
            "reasoning": {
                "clinician_summary": result.get("clinician_summary"),
                "full_explanation": result.get("full_explanation"),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clinician/review")
def clinician_review(payload: ClinicianReview):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "patient_id": payload.patient_id,
        "model_risk_score": payload.model_risk_score,
        "decision_mode": payload.decision_mode,
        "clinician_decision": payload.clinician_decision,
        "clinician_notes": payload.clinician_notes
    }

    with open("hitl_audit_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "status": "recorded",
        "patient_id": payload.patient_id,
        "final_decision": payload.clinician_decision, 
        "notes": payload.clinician_notes
    }


@router.get("/review/queue")
def review_queue():
    return {
        "pending_reviews": [
            {
                "patient_id": "demo_001",
                "risk_score": 0.82,
                "decision_mode": "SAFE",
                "reason": "Low confidence – HITL required"
            }
        ]
    }


@router.get("/metadata")
def metadata():
    return {
        "model_version": "ckd_model_v1",
        "pipeline_version": "genai_pipeline_v1",
        "llm_provider": "groq",
        "llm_model": "llama-3.1-8b-instant"
    }
