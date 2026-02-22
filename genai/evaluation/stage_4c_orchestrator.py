# genai/evaluation/stage_4c_orchestrator.py

from genai.evaluation.load_shap_artifacts import load_shap_artifacts
from genai.retrieval.retriever import search
from genai.retrieval.retrieval_adapter import format_retrieved_chunks
from genai.prompts.shap_adapter import format_shap_features
import logging


def compute_confidence(risk_score: float) -> float:
    """
    Confidence proxy:
    Lower confidence near decision boundary (0.5)
    """
    return max(0.0, 1 - abs(risk_score - 0.5) * 2)


def decide_mode(confidence: float):
    if confidence < 0.30:
        return "SAFE"
    elif confidence < 0.65:
        return "VERBOSE"
    else:
        return "NORMAL"


def run_stage_4c(input_data: dict, risk_score: float):

    # SAFETY ASSERTION — risk propagation integrity
    assert isinstance(risk_score, (float, int)), "Risk score must be numeric"
    assert 0.0 <= risk_score <= 1.0, "Risk score out of expected range"

    # 1. Load ML + SHAP outputs
    try:
        _, shap_features = load_shap_artifacts() 
    except Exception:
        shap_features = {}

    # 2. Confidence tagging (explicit)
    confidence = float(round(compute_confidence(risk_score), 3))

    # 3. Evidence retrieval
    query = "chronic kidney disease risk factors"
    retrieved = search(query, k=3)
    retrieval_count = len(retrieved)


    # 4. Explanation preparation
    shap_text = format_shap_features(shap_features)
    if shap_text is None or shap_text.strip() == "":
        shap_text = "SHAP explanation unavailable."

    shap_explanation: str = shap_text
    retrived_evidence: str = ""

    #Confidence calculation (robust)

    certainty = abs(risk_score - 0.5) * 2

    shap_signal = 1 if shap_text and "unavailable" not in shap_text.lower() else 0
    retrieval_signal = 1 if retrieved else 0

    confidence = 0.7 * certainty + 0.15 * shap_signal + 0.15 * retrieval_signal

    if 0.45 <=risk_score <=0.55:
        confidence *=0.9

    if shap_signal == 0 and retrieval_signal == 0:
        confidence *= 0.92
    confidence = round(confidence, 3)

    decision_mode = decide_mode(confidence)

    if decision_mode == "SAFE":
        logging.warning(
            f"SAFE Mode triggered - human clinician review recommended | confidence={confidence} | risk_score={risk_score}"
        )
        
        shap_explanation = (
            "⚠️ System safety guard triggered. "
            "Explanation suppressed due to low system reliability. "
            "Human review recommended."
        )
        retrieved_evidence = "Evidence retrieval suppressed due to low confidence."

    elif decision_mode == "VERBOSE":

            shap_explanation = (
                "⚠️ Moderate confidence detected. "
                "The following explanation is probabilistic and should be "
                "interpreted cautiously.\n\n"
                + shap_text
            )
            retrieved_evidence = format_retrieved_chunks(retrieved)

    else:
        shap_explanation = shap_text
        retrieved_evidence = format_retrieved_chunks(retrieved)        

    # 6. Final payload (authoritative)
    payload = {
        "risk_score": round(risk_score, 4),
        "confidence": confidence,
        "decision_mode": decision_mode,
        "guarded_output": {
            "decision_mode": decision_mode,
        },
        "shap_explanation": shap_explanation,
        "retrieved_evidence": retrieved_evidence,
    }

    return payload
