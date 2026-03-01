# Robustness & Distribution Shift Analysis

## Objective

Test model stability under simulated distribution shift.

---

## Method

- Injected Gaussian noise (μ=0, σ=0.05) into feature space.
- Recomputed AUC on perturbed dataset.

---

## Results

- Original AUC: 0.9994
- Noisy AUC: 0.6629
- AUC Drop: 0.3364

---

## Interpretation

- Model sensitive to feature perturbation.
- Indicates vulnerability to real-world distribution drift.
- Motivated addition of:
  - Confidence tagging
  - HITL override
  - Guardrails

---

## Engineering Implication

Production systems must include:
- Drift detection
- Confidence thresholds
- Human review mechanisms

