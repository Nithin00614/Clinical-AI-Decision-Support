# genai/evaluation/stage_4c_orchestrator.py
from genai.retrieval.retriever import search
from genai.retrieval.retrieval_adapter import format_retrieved_chunks
from genai.prompts.shap_adapter import format_shap_features
from genai.explainability.clinical_shap_translator import translate_shap
from genai.explainability.shap_formatter import build_structured_shap
from genai.explainability.clinical_shap_translator import generate_clinical_sentences
from genai.explainability.shap_loader import load_expected_features
from genai.evaluation.reasoning_controller import (compute_certainty, decide_mode, detect_explanation_mismatch)
import logging



def run_stage_4c(input_data: dict, risk_score: float, shap_features: dict):

    # SAFETY ASSERTION — risk propagation integrity
    assert isinstance(risk_score, (float, int)), "Risk score must be numeric"
    assert 0.0 <= risk_score <= 1.0, "Risk score out of expected range"

    risk_score = float(risk_score)
    

    # 2. Evidence retrieval
    query = "chronic kidney disease risk factors"
    retrieved = search(query, k=3)
    retrieval_count = len(retrieved)


    # 3. Explanation preparation
    shap_text = format_shap_features(shap_features)
    if shap_text is None or shap_text.strip() == "":
        shap_text = "SHAP explanation unavailable."

    shap_explanation: str = shap_text
    retrived_evidence: str = ""


    shap_features = {k: float(v) for k,v in shap_features.items()}
    try:
        structured_shap = build_structured_shap(shap_features)
    except Exception:
        structured_shap = {
            "top_positive": [],
            "top_negative": [],
            "vector_available": False
        }

    expected_features = load_expected_features()    
    missing_features = set(expected_features) - set(shap_features.keys())
    shap_missing_features = list(missing_features)
    shap_available = bool(shap_features)
    shap_mismatch = False


    print("certainty:", certainty)
    print("shap_signal:", shap_signal)
    print("retrieval_signal:", retrieval_signal)
    print("final confidence:", confidence)


    logging.info(f"STAGE$ SHAP: {shap_features}")
    decision_mode = decide_mode(confidence)

    if decision_mode == "SAFE":
        logging.warning(
            f"SAFE Mode triggered - human clinician review recommended | confidence={confidence} | risk_score={risk_score}"
        )
        
        shap_explanation = (
            "⚠️ Low confidence prediction.\n"
            "Top contributing factors are shown for clinician review only:\n\n"
            + shap_text
        )
        retrieved_evidence = "Evidence retrieval suppressed due to low confidence."

    elif decision_mode == "VERBOSE":
            safe_shap = shap_text or "SHAP unavailable"

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
        "shap": structured_shap,
        "shap_missing_features": shap_missing_features,
        "shap_available": shap_available,
        "shap_mismatch": shap_mismatch,
        "cinical_factors": clinical_sentences,
        "explanation_available": structured_shap["vector_available"],
        "guarded_output": {
            "decision_mode": decision_mode,
        },
        "shap_explanation": shap_explanation,
        "retrieved_evidence": retrieved_evidence,
    }

    return payload
