# genai/evaluation/stage_4c_orchestrator.py

from genai.evaluation.load_shap_artifacts import load_shap_artifacts
from genai.retrieval.retriever import search
from genai.retrieval.retrieval_adapter import format_retrieved_chunks
from genai.prompts.shap_adapter import format_shap_features


def compute_confidence(risk_score: float) -> float:
    """
    Confidence proxy:
    Lower confidence near decision boundary (0.5)
    """
    return max(0.0, 1 - abs(risk_score - 0.5) * 2)


def decide_mode(confidence: float, retrieval_count: int) -> str:
    if confidence >= 0.7 and retrieval_count >= 2:
        return "NORMAL"
    elif confidence >= 0.4:
        return "VERBOSE"
    else:
        return "SAFE"


def run_stage_4c(input_data: dict, risk_score: float):
    # 1. Load ML + SHAP outputs
    risk_score, shap_features = load_shap_artifacts()

    # 2. Confidence tagging (explicit)
    confidence = round(compute_confidence(risk_score), 3)

    # 3. Evidence retrieval
    query = "chronic kidney disease risk factors"
    retrieved = search(query, k=3)
    retrieval_count = len(retrieved)

    # 4. System decision
    decision_mode = decide_mode(confidence, retrieval_count)

    # 5. Explanation preparation
    shap_text = format_shap_features(shap_features)

    if decision_mode == "SAFE":
        shap_explanation = (
            "⚠️ Model confidence is low. "
            "No clinical reasoning is generated. "
            "Human review is required."
        )
        retrieved_evidence = ""

    else:
        retrieved_evidence = format_retrieved_chunks(retrieved)
        shap_explanation = shap_text

        if decision_mode == "VERBOSE":
            shap_explanation = (
                "⚠️ Moderate confidence detected. "
                "The following explanation is probabilistic and should be "
                "interpreted cautiously.\n\n"
                + shap_explanation
            )

    # 6. Final payload (authoritative)
    payload = {
        "risk_score": round(risk_score, 4),
        "confidence": confidence,
        "guarded_output": {
            "decision_mode": decision_mode,
        },
        "shap_explanation": shap_explanation,
        "retrieved_evidence": retrieved_evidence,
    }

    return payload
