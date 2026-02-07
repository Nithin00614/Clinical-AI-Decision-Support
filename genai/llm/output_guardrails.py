# genai/llm/output_guardrails.py

FORBIDDEN_PATTERNS = [
    "diagnose",
    "treatment",
    "prescribe",
    "should take",
    "recommended therapy",
]

def apply_output_guardrails(
    llm_text: str,
    decision_mode: str,
    confidence: float | None = None,
):
    # 1. Hard safety check
    lowered = llm_text.lower()
    for phrase in FORBIDDEN_PATTERNS:
        if phrase in lowered:
            return {
                "mode": "BLOCKED",
                "reason": "Unsafe clinical recommendation detected",
                "text": (
                    "This system cannot provide medical advice.Please consult a qualified healthcare professional."
                ),
            }

    # 2. Mode-based restriction
    if decision_mode == "safe":
        return {
            "mode": "SAFE_MODE",
            "text": (
                "The system is operating in Safe Observation Mode. "
                "Automated reasoning is withheld due to uncertainty. "
                "Human clinical review is required."
            ),
        }

    # 3. Confidence-aware disclaimer
    if confidence is not None and confidence < 0.6:
        llm_text += (
            "\n\nNote: Model confidence is low. "
            "This explanation should be interpreted cautiously."
        )

    # 4. Normal pass-through
    return {
        "mode": "NORMAL",
        "text": llm_text,
    }
