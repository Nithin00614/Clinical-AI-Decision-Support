from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.llm_prompt_builder import build_llm_prompt
from genai.controller.system_controller import decide_mode
from genai.llm.output_guardrails import apply_output_guardrails
from genai.llm.llm_client import GroqLLMClient
import re

def build_clinician_summary(text: str) -> str:
    if not text:
        return "Clinical review recommended."

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # remove very long evidence paragraphs
    lines = [l for l in lines if len(l) < 160]

    summary = " ".join(lines[:3])

    # force 2 sentences max
    sentences = [s.strip() for s in summary.split(".") if s.strip()]
    summary = ". ".join(sentences[:2])

    if not summary.endswith("."):
        summary += "."

    return summary

def split_references(text: str):
    lower = text.lower()

    ref_markers = ["references:", "kdigo", ".pdf", "study", "trial"]

    for marker in ref_markers:
        idx = lower.find(marker)
        if idx != -1 and idx > len(text) * 0.4:
            body = text[:idx]
            refs = text[idx:]
            return body.strip(), refs.strip()

    return text.strip(), None

def structure_explanation(text: str) -> str:
    if not text:
        return ""

    sections = [
        "### Risk Interpretation\n",
        "### Key Contributing Factors\n",
        "### Clinical Uncertainty\n",
        "### Suggested Clinical Action\n",
    ]

    parts = text.split("\n\n")

    structured = ""
    for i, part in enumerate(parts):
        if i < len(sections):
            structured += sections[i] + part + "\n\n"
        else:
            structured += part + "\n\n"

    return structured.strip()  

def run_llm_stage(stage4):
    # 1) Get grounded payload (Stage 4C)
    payload = stage4
    
    # 2a) Decide system mode (System Controller)
    decision_mode = stage4.get("decision_mode", "NORMAL")
    confidence = stage4.get("confidence", 0.0)

    # 3) Build LLM prompt
    system_prompt, user_prompt = build_llm_prompt(payload)

    # 4) Call real LLM
    llm = GroqLLMClient()

    explanation = llm.generate(system_prompt, user_prompt)
    clinician_summary = ""
    if decision_mode == "SAFE":
        explanation = ("System reliability is limited."
                       "Automated reasoning is restricted and clinician review is recommended.")
        clinician_summary = explanation
        explanation_body = explanation
        references = ""


    else:
        explanation_body, references = split_references(explanation) 
        clinician_summary = build_clinician_summary(explanation_body)

    original_llm_text = explanation
    if not explanation_body:
        explanation_body = original_llm_text

    explanation_body = structure_explanation(explanation_body)
     # 5) output guardrails
    guarded = apply_output_guardrails(
        llm_text=explanation_body,
        decision_mode=decision_mode,
        confidence=confidence,
    )


    #  SAFE MERGE
    if isinstance(guarded, dict):
        extracted = guarded.get("full_text") or guarded.get("text")
        if extracted and extracted.strip():
            explanation_body = extracted
    elif isinstance(guarded, str) and guarded.strip():
        explanation_body = guarded

    if not explanation_body:
        explanation_body = original_llm_text

    reasoning_metadata = {
    "llm_used": True,
    "evidence_used": bool(payload.get("retrieved_evidence")),
    "shap_used": bool(payload.get("shap_explanation")),
    "guardrail_mode": guarded.get("mode") if isinstance(guarded, dict) else "UNKNOWN",
}

    return {
    "risk_score": payload["risk_score"],
    "confidence": payload["confidence"],
    "decision_mode": decision_mode,
    "shap_explanation": payload.get("shap_explanation"),
    "retrieved_evidence": payload.get("retrieved_evidence"),
    "clinician_summary": clinician_summary,
    "full_explanation": explanation_body,
    "references": references,
    "reasoning_metadata": reasoning_metadata
}



if __name__ == "__main__":
    output = run_llm_stage()
    print("\nFinal Explanation:\n")
    print(output["full_explanation"])
    if output["references"]:
        print("\nReferences:\n")
        print(output["references"])
