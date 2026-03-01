
# Evaluation Protocol

## Internal Holdout Evaluation

20% of dataset reserved as test cohort.

### Metrics

- AUC: 0.9994
- F1: 0.9859
- Accuracy: 0.9825
- Sensitivity: 0.98
- Specificity: 0.9866
- Brier Score: 0.0186

---

## Interpretation

- Strong linear separability in dataset
- Logistic regression sufficient
- Low calibration error

---

## Caution

High performance likely influenced by:
- Small dataset size
- Strong predictor dominance (Sc, Bu, Hemo, Htn)

