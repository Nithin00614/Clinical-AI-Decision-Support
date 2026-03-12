def build_llm_prompt(payload: dict):
    """
    Build LLM prompt using the clinical reasoning template.
    This ensures the LLM is explicitly instructed to follow the structured output format.
    """
    from genai.prompts.clinical_reasoning_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
    
    mode = payload.get("decision_mode", "normal").lower()
    confidence = payload.get("confidence", 0.0)
    risk_score = payload.get("risk_score", 0.0)
    risk_label = payload.get("risk_label", "UNKNOWN")
    
    # Format SHAP features for display
    shap_data = payload.get("shap") or {}
    top_positive = shap_data.get("top_positive", [])
    top_negative = shap_data.get("top_negative", [])
    
    shap_features_str = "Top Risk Drivers:\n"
    for item in top_positive[:5]:
        shap_features_str += f"  - {item.get('feature')}: +{item.get('impact'):.4f}\n"
    
    shap_features_str += "                               \nProtective Drivers:\n"
    for item in top_negative[:5]:
        shap_features_str += f"  - {item.get('feature')}: {item.get('impact'):.4f}\n"
    
    driver_list = [d.get("feature") for d in (top_positive + top_negative)]
    driver_list_str = ", ".join(driver_list[:10]) if driver_list else "N/A"
    
    # Format clinical evidence
    retrieved_evidence = payload.get("retrieved_evidence", [])
    if isinstance(retrieved_evidence, list):
        evidence_str = "\n".join([f"  • {e}" for e in retrieved_evidence[:5]])
    else:
        evidence_str = str(retrieved_evidence)[:500]
    
    clinical_shap_summary = payload.get("clinical_shap_summary", "")
    shap_mismatch = payload.get("shap_mismatch", False)
    shap_missing_features = payload.get("shap_missing_features", [])
    
    # Special handling for SAFE mode
    if mode == "safe":
        system_prompt = (
            "You are a clinical explanation assistant in SAFE mode.\n"
            "System reliability is limited. Do NOT provide detailed reasoning.\n"
            "State that human clinical review is required.\n"
        )
        user_prompt = (
            "Due to limited system reliability or unclear risk signals, "
            "automated reasoning is restricted.\n\n"
            "Response: Recommend clinician review. Automated explanation unavailable."
        )
        return system_prompt, user_prompt
    
    # Use template for NORMAL and VERBOSE modes
    system_prompt = SYSTEM_PROMPT
    
    # Build user prompt from template
    user_prompt = USER_PROMPT_TEMPLATE.format(
        risk_label=risk_label,
        risk_score=risk_score,
        display_risk_score=payload["display_risk_score"],
        shap_features=shap_features_str,
        driver_list=driver_list_str,
        clinical_shap_summary=clinical_shap_summary,
        shap_mismatch="Yes - explanation uncertainty expected" if shap_mismatch else "No",
        shap_missing_features=", ".join(shap_missing_features) if shap_missing_features else "None",
        retrieved_evidence_llm=evidence_str if evidence_str else "No clinical evidence retrieved"
    )
    
    return system_prompt, user_prompt
