from genai.prompts.clinical_reasoning_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from genai.prompts.shap_adapter import format_shap_features
from genai.retrieval.retrieval_adapter import format_retrieved_chunks


def build_reasoning_prompt(risk_score: float, shap_dict: dict, retrieved_chunks: list):

   # ---------- SHAP formatting ----------
    if shap_dict:
        shap_text = format_shap_features(shap_dict)
    else:
        shap_text = "No SHAP explanation available."

    # disclaimer about SHAP interpretation
    shap_text = (
        "SHAP values reflect statistical feature influence on the model prediction "
        "and should not be interpreted as causal clinical relationships.\n\n"
        + shap_text
    )

    # ---- Retrieval ----
    if retrieved_chunks:
        evidence_text = format_retrieved_chunks(retrieved_chunks)
    else:
        evidence_text = "No guideline evidence retrieved."

    user_prompt = USER_PROMPT_TEMPLATE.format(
        risk_score=float(risk_score),
        shap_features=shap_text,
        retrieved_evidence=evidence_text,
    )

    return SYSTEM_PROMPT, user_prompt