# Failure Modes & Mitigations

## 1. SHAP Unavailable or Mismatch
*Issue*
- SHAP values missing or feature mismatch

*Impact*
- No reliable explanation drivers

*Mitigation*
- Skip SHAP explanation
- Reduce confidence
- Trigger SAFE mode

---

## 2. Retrieval Failure
*Issue*
- No clinical evidence retrieved

*Impact*
- LLM lacks grounding → hallucination risk

*Mitigation*
- Set retrieval_signal = 0
- Reduce confidence
- Allow reasoning with uncertainty OR SAFE fallback

---

## 3. LLM Hallucination (Feature Drift)
*Issue*
- LLM introduces features not in SHAP drivers

*Impact*
- Misaligned explanation

*Mitigation*
- validate_feature_alignment()
- Force SAFE mode if violated

---

## 4. Low Explanation Coverage
*Issue*
- LLM does not explain all important drivers

*Impact*
- Partial / misleading explanation

*Mitigation*
- compute_explanation_coverage()
- Reduce reliability score

---

## 5. Low Explanation Reliability
*Issue*
- Weak traceability + low coverage

*Impact*
- Untrustworthy reasoning

*Mitigation*
- compute_explanation_reliability()
- Auto switch to SAFE mode

---

## 6. Overconfident Predictions
*Issue*
- High risk score but weak explanation support

*Impact*
- Unsafe clinical decision

*Mitigation*
- confidence calibration
- high-risk confidence cap (≤ 0.93)

---

## 7. Guardrail Blocking
*Issue*
- Output violates safety constraints

*Impact*
- No usable explanation

*Mitigation*
- fallback explanation
- SAFE mode response

---

## 8. Data Shift / Input Drift
*Issue*
- Input data distribution changes

*Impact*
- Model predictions unreliable

*Mitigation*
- schema validation
- monitoring hooks (future work)


---