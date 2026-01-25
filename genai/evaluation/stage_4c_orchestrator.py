# genai/evaluation/stage_4c_orchestrator.py

from genai.evaluation.load_shap_artifacts import load_shap_artifacts
from genai.retrieval.retriever import search
from genai.retrieval.retrieval_adapter import format_retrieved_chunks
from genai.prompts.shap_adapter import format_shap_features
from genai.evaluation.confidence_tagging import assign_confidence


def run_stage_4c():
    """
    Stage 4C Orchestrator:
    - Load real SHAP outputs
    - Retrieve real guideline evidence via FAISS
    - Format SHAP + evidence
    - Assign confidence
    - Return unified payload for LLM + evaluation
    """

    # 1) Load REAL SHAP artifacts
    risk_score, shap_features = load_shap_artifacts()

    # 2) Build retrieval query from top SHAP features
    top_features = list(shap_features.keys())[:3]
    query = " ".join(top_features)

    # 3) Retrieve REAL guideline chunks
    retrieval_results = search(query, k=3)

    # 4) Format for prompts
    shap_explanation = format_shap_features(shap_features)
    retrieved_evidence = format_retrieved_chunks(retrieval_results)

    # 5) Assign confidence
    confidence = assign_confidence(
        risk_score=risk_score,
        shap_features=shap_features,
        retrieved_chunks=retrieval_results
    )

    # 6) Build payload (THIS WAS MISSING)
    payload = {
        "risk_score": risk_score,
        "shap_explanation": shap_explanation,
        "retrieved_evidence": retrieved_evidence,
        "confidence": confidence
    }

    return payload
