from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.llm_prompt_builder import build_llm_prompt
from genai.controller.system_controller import decide_mode
from genai.llm.output_guardrails import apply_output_guardrails
from genai.llm.llm_client import GroqLLMClient
from genai.llm.llm_postprocess import (build_clinician_summary, split_references, structure_explanation)


def run_llm_stage(stage4):
    # 1) Get grounded payload (Stage 4C)
    payload = dict(stage4)
    
    # 2a) Decide system mode (System Controller)
    decision_mode = stage4.get("decision_mode", "NORMAL")
    confidence = stage4.get("confidence", 0.0)

    payload["shap_features"] = payload.get("shap", {})
    payload["clinical_shap_summary"] = ""
    payload["shap_mismatch"] = payload.get("shap_mismatch", False)
    payload["shap_missing_features"] = payload.get("shap_missing_features", [])

    # 3) Build LLM prompt
    system_prompt, user_prompt = build_llm_prompt(payload)

    # 4) Call real LLM
    llm = GroqLLMClient()

    explanation = llm.generate(system_prompt, user_prompt)
    if not explanation or not explanation.strip():
        explanation = "Model produced no explanation. SHAP evidence suggests: " + payload.get("clinical_shap_summary", "")

    clinician_summary = ""
    if decision_mode == "SAFE":
        explanation = ("System reliability is limited."
                       "Automated reasoning is restricted and clinician review is recommended.")
        clinician_summary = explanation
        explanation_body = explanation
        references = ""


    else:
        explanation_body, references = split_references(explanation) 
        clinician_summary = build_clinician_summary("", payload)

    # Ensure clinician summary is concise and not SHAP repetition
    if clinician_summary:
        clinician_summary = clinician_summary.replace("\n", " ").strip()

        if len(clinician_summary) > 200:
            clinician_summary = clinician_summary[:200].rsplit(".", 1)[0] + "."
    
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

    # Explainability health
    explanation_present = bool(explanation_body and explanation_body.strip())

    shap_struct = payload.get("shap") or payload.get("shap_features")
    shap_present = (isinstance(shap_struct,dict) and shap_struct.get("vector_available", False))

    guard_blocked = isinstance(guarded, dict) and guarded.get("mode") in ["BLOCKED", "EMPTY"]

    if guard_blocked or not explanation_present:
        explainability_status = "Unavailable"

    elif explanation_present and shap_present:
        explainability_status = "Available"

    else:
        explainability_status = "Degraded"


    if explainability_status == "Unavailable":
        reasoning_confidence = "LOW"

    elif explainability_status == "Degraded":
        reasoning_confidence = "MEDIUM"

    else:
        reasoning_confidence = "HIGH"


    reasoning_metadata = {
    "llm_used": True,
    "llm_fallback": explanation.startswith("System reliability is limited"),
    "evidence_used": bool(payload.get("retrieved_evidence")),
    "shap_used": bool(payload.get("shap_features")),
    "confidence_score": confidence,
    "decision_mode": decision_mode,
    "retrieval_used": bool(payload.get("retrieved_evidence")),
    "guardrail_mode": guarded.get("mode") if isinstance(guarded, dict) else "UNKNOWN",
    "explainability_status": explainability_status,
    "reasoning_confidence": reasoning_confidence,
}

    print("metadata:", reasoning_metadata)
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
