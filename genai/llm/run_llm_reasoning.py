from genai.evaluation.stage_4c_orchestrator import run_stage_4c
from genai.llm.llm_prompt_builder import build_llm_prompt
from genai.llm.llm_client import GroqLLMClient


def run_llm_stage():
    # 1) Get grounded payload (Stage 4C)
    payload = run_stage_4c()

    # 2) Build LLM prompt
    system_prompt, user_prompt = build_llm_prompt(payload)

    # 3) Call real LLM
    llm = GroqLLMClient()
    explanation = llm.generate(system_prompt, user_prompt)

    return {
        "risk_score": payload["risk_score"],
        "confidence": payload["confidence"],
        "explanation": explanation
    }


if __name__ == "__main__":
    output = run_llm_stage()
    print("\nFinal Explanation:\n")
    print(output["explanation"])
