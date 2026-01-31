def build_llm_prompt(payload: dict):
    system_prompt = (
        "You are a clinical explanation assistant.\n"
        "Use ONLY the provided information.\n"
        "Do NOT diagnose or recommend treatment.\n"
        "If evidence is insufficient, state this clearly.\n"
    )

    user_prompt = f"""
Risk Probability:
{payload['risk_score']}

Model Explanation (SHAP):
{payload['shap_explanation']}

Clinical Evidence:
{payload['retrieved_evidence']}

Confidence:
Level: {payload['confidence']['confidence_level']}
Note: {payload['confidence']['confidence_note']}

Task:
Provide a clear, evidence-grounded explanation of the risk.
Do not provide medical advice.
"""

    return system_prompt, user_prompt
