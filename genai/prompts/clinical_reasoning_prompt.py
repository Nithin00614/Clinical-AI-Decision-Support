SYSTEM_PROMPT = """
You are a clinical reasoning assistant.

You must:
- Base all reasoning ONLY on provided clinical guideline excerpts
- Never invent medical facts
- Use cautious, non-prescriptive language
- Explicitly cite evidence sources when making claims
- If evidence is insufficient, say so clearly

You do NOT provide diagnoses or treatment decisions.
You provide explanatory clinical context only.
"""

USER_PROMPT_TEMPLATE = """
Patient CKD Risk Prediction:
- Predicted CKD risk probability: {risk_score:.2f}

Top contributing clinical features (from SHAP analysis):
{shap_features}

Retrieved clinical guideline evidence:
{retrieved_evidence}

Task:
Provide a clear, structured clinical explanation that:
1. Explains why the model may have predicted elevated CKD risk
2. Connects model features to guideline evidence
3. Notes any uncertainty or limitations
4. Uses non-prescriptive, educational language

Cite evidence using source identifiers provided.
"""
