def build_llm_prompt(payload: dict):
    mode = payload.get("decision_mode", "normal").lower()
    confidence = payload.get("confidence", 0.0)

    system_prompt = (
        "You are a clinical explanation assistant.\n"
        "Use ONLY the provided information.\n"
        "Do NOT diagnose or recommend treatment.\n"
        "If evidence is insufficient, state this clearly.\n"
    )

    if mode == "safe":
        system_prompt += (
            "\nSYSTEM MODE: SAFE\n"
            "Do NOT provide reasoning.\n"
            "State that human clinical review is required.\n"
        )

    elif mode == "verbose":
        system_prompt += (
            "\nSYSTEM MODE: VERBOSE\n"
            "Provide detailed explanation.\n"
            "Explicitly discuss uncertainty and limitations.\n"
        )

    user_prompt = f"""
Risk Probability:
{payload['risk_score']}

Model Explanation (SHAP):
{payload['shap_explanation']}

Clinical Evidence:
{payload['retrieved_evidence']}

Confidence Score:
{confidence}

Task:
Provide a clear, evidence-grounded explanation of the risk.
Do not provide medical advice.
"""

    return system_prompt, user_prompt
