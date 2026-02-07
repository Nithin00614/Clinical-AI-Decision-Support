from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.llm_prompt_builder import build_llm_prompt
from genai.controller.system_controller import decide_mode
from genai.llm.output_guardrails import apply_output_guardrails
from genai.llm.llm_client import GroqLLMClient


def run_llm_stage():
    # 1) Get grounded payload (Stage 4C)
    payload = run_stage_4c()

    # 2a) Decide system mode (System Controller)
    decision_mode = decide_mode(payload)
    payload["decision_mode"] = decision_mode

    # 3) Build LLM prompt
    system_prompt, user_prompt = build_llm_prompt(payload)

    # 4) Call real LLM
    llm = GroqLLMClient()
    explanation = llm.generate(system_prompt, user_prompt)

    # 5) output guardrails
    guarded = apply_output_guardrails(
        llm_text=explanation,
        decision_mode=payload.get("decision_mode", "NORMAL"),
        confidence=payload.get("confidence"),
    )

    return {
        "risk_score": payload["risk_score"],
        "confidence": payload["confidence"],
        "shap_explanation": payload.get("shap_explanation"),
        "retrieved_evidence": payload.get("retrieved_evidence"),    
        "explanation": explanation,
        "guarded_output": guarded
    }



if __name__ == "__main__":
    output = run_llm_stage()
    print("\nFinal Explanation:\n")
    print(output["explanation"])
