import logging
from fastapi import APIRouter, HTTPException
from api.schemas import PatientInput

from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services1.inference_service import predict_patient
from services1.reasoning_service import run_reasoning

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
            },
            "explainability": {
                "shap_explanation": result.get("shap_explanation"),
                "retrieved_evidence": result.get("retrieved_evidence"),
            },
            "reasoning": {
                "llm_explanation": result.get("guarded_output",{}).get("text"),
                "full_explanation": result.get("explanation"),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata")
def metadata():
    return {
        "model_version": "ckd_model_v1",
        "pipeline_version": "genai_pipeline_v1",
        "llm_provider": "groq",
        "llm_model": "llama-3.1-8b-instant"
    }
