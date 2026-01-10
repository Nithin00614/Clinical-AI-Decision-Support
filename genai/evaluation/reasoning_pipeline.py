from genai.prompts.clinical_reasoning_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from genai.prompts.shap_adapter import format_shap_features
from genai.retrieval.retrieval_adapter import format_retrieved_chunks

def build_reasoning_prompt(
    risk_score: float,
    shap_dict: dict,
    retrieved_chunks: list
):
    shap_text = format_shap_features(shap_dict)
    evidence_text = format_retrieved_chunks(retrieved_chunks)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        risk_score=risk_score,
        shap_features=shap_text,
        retrieved_evidence=evidence_text
    )

    return SYSTEM_PROMPT, user_prompt
