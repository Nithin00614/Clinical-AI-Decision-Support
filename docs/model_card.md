# Model Card – CKD Clinical AI Decision Support System

## Model Overview

- Model Type: Logistic Regression (Calibrated)
- Training Dataset Size: 400 patients
- Features Used: 13 structured clinical indicators
- Output: CKD Risk Probability (0–1)

---

## Intended Use

This model is designed for:

- Clinical decision support
- Risk stratification assistance
- Educational demonstrations of AI reasoning pipelines

It is NOT intended for:

- Autonomous medical decision-making
- Emergency triage
- Replacement of physician judgment

---

## Performance (Internal Validation)

- AUC: 0.9994
- F1 Score: 0.9859
- Accuracy: 0.9825
- Brier Score: 0.0186

Dataset shows high linear separability.

---

## Explainability

- SHAP-based feature attribution
- Structured clinical interpretation layer
- LLM-based contextual reasoning
- Guardrails to prevent unsupported claims

---

## Confidence System

Final confidence combines:

- Model certainty (distance from 0.5)
- SHAP availability
- Retrieval evidence presence

Confidence ≠ probability.

---

## Robustness Findings

Under Gaussian perturbation:

- AUC dropped from 0.9994 to 0.6629

Indicates sensitivity to distribution shift.

System mitigations include:

- Confidence tagging
- Human-in-the-loop override
- Decision mode controller

---

## Ethical Considerations

- Small dataset
- Potential sampling bias
- Requires clinician review for deployment

---

## Monitoring Strategy

Future production version should include:

- Drift detection
- Calibration monitoring
- Periodic retraining

---

## Version

Model Version: v1.0.0  
Last Updated: [1-03-2026]

