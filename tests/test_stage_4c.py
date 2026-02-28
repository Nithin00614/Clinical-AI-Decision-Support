from genai.evaluation.stage_4c_orchestrator import run_stage_4c

if __name__ == "__main__":
    payload = run_stage_4c()

    print("\n✔ Stage 4C Validation\n")
    print("Risk score:", payload["risk_score"])
    print("\nSHAP explanation (sample):\n", payload["shap_explanation"][:300])
    print("\nRetrieved evidence (sample):\n", payload["retrieved_evidence"][:300])
    print("\nConfidence:")
    print(payload.get("confidence", "Confidence not attached yet"))


