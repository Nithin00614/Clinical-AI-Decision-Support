# genai/llm/output_guardrails.py
import logging


def apply_output_guardrails(
    llm_text: str,
    decision_mode: str,
    confidence: float | None = None,
):
   
    if not llm_text:
        return {
            "mode":"EMPTY",
            "text":"",
            "full_text":""
        }

    # 1. Hard safety check
    lowered = llm_text.lower()
    directive_words = [
    "you should",
    "start",
    "must take",
    "begin",
    "prescribe",
    "initiate",
]

    clinical_action_words = [
        "drug",
        "medication",
        "dose",
        "dosage",
        "tablet",
        "therapy",
        "treatment",
        "injection",
    ]

    directive_present = any(w in lowered for w in directive_words)
    action_present = any(w in lowered for w in clinical_action_words)

    if directive_present and action_present:
        logging.warning("Guardrail triggered directive therapeutic recommendation")
        return {
            "mode": "BLOCKED",
            "reason": "Directive therapeutic recommendation detected",
            "text": (
                "Automated therapeutic recommendations are restricted. "
                "This system provides clinical decision support only. "
                "Final treatment decisions must remain clinician-authoritative."
            ),
            "full_text": ""
        }

    # 2. Mode-based restriction
    if decision_mode.upper() == "SAFE":
        return {
            "mode": "SAFE_MODE",
            "text": (
                "The system is operating in uncertainty-aware observation mode. "
                "Automated reasoning is intentionally constrained due to limited confidence. "
                "Clinical review is recommended before action."
            ),
        }

    # 3. Confidence-aware disclaimer
    if confidence is not None and confidence < 0.6:
        llm_text += (
            "\n\nNote: Model confidence is low. "
            "This explanation should be interpreted cautiously."
        )

    # 4. Normal pass-through

    short_summary = " ".join(llm_text.split(".")[:2]) + "."
    short_summary = short_summary[:300]

    return {
        "mode": "NORMAL",
        "text": short_summary,     # clinician short explanation
        "full_text": llm_text      # full reasoning
    }