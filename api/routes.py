import logging
from fastapi import APIRouter, HTTPException
from api.schemas import PatientInput

from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.run_llm_reasoning import run_llm_stage
from services1.inference_service import predict_patient

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
def reasoning_api():
    try:
        result = run_llm_stage()

        return {
            "prediction": {
                "risk_score": result["risk_score"],
                "confidence": result["confidence"],
                "decision_mode": result["guarded_output"]["mode"]
            },
            "explainability": {
                "shap_explanation": result.get("shap_explanation"),
                "retrieved_evidence": result.get("retrieved_evidence")
            },
            "reasoning": {
                "llm_explanation": result["guarded_output"]["text"],
                "full_explanation": result.get("explanation")
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
