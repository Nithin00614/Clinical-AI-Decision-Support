# Data Shift and Robustness Analysis

## 1. Purpose

Machine learning models may experience performance degradation when deployed in environments where the input data distribution differs from the training data.

This document describes potential **data shift risks**, robustness evaluation conducted during development, and mitigation mechanisms implemented within the CKD clinical decision-support system.

---

## 2. Distribution Shift in Clinical Machine Learning

**Distribution shift** occurs when the statistical properties of real-world inputs differ from those seen during model training.

In healthcare systems, this may occur due to:

- different patient populations
- changes in laboratory measurement practices
- variation in data collection protocols
- missing or inconsistent clinical records

Such shifts may reduce model reliability and increase prediction uncertainty.

---

## 3. Potential Sources of Data Shift

In CKD risk prediction systems, distribution shift may arise from several factors:

**Population Variability**

- differences in patient demographics
- varying prevalence of CKD across clinical settings

**Laboratory Measurement Variability**

- differences in laboratory calibration
- measurement precision differences between hospitals

**Feature Availability**

- missing laboratory values
- incomplete patient records

**Clinical Practice Variations**

- hospital-specific testing procedures
- differences in diagnostic thresholds

These factors may affect the reliability of model predictions if not monitored.

---

## 4. Robustness Evaluation Method

To evaluate model robustness, a **Gaussian noise perturbation test** was performed.

Procedure:

1. Random Gaussian noise was added to the input feature distributions.
2. The perturbed dataset was passed through the trained prediction pipeline.
3. Performance metrics were compared against the original dataset.

This simulation approximates the effect of **measurement noise and distribution changes**.

---

## 5. Robustness Results

The perturbation test revealed sensitivity to distribution changes.

| Metric | Baseline | Perturbed Data |
|--------|----------|----------------|
| AUC | 0.9994 | 0.6629 |

Observed AUC reduction:

```
AUC Drop: 0.3364
```

Interpretation:

- the model relies heavily on dominant predictive features
- performance degrades under distribution shift
- monitoring mechanisms are required for real-world deployment

---

## 6. System-Level Mitigations

The system incorporates several mechanisms to reduce risks associated with distribution shift.

**Confidence Scoring**

Prediction reliability is estimated using:

- model certainty (distance from decision boundary)
- explainability availability
- evidence retrieval signals

**Decision Mode Controller**

The reasoning system operates in different modes:

| Mode | Behavior |
|------|----------|
| SAFE | explanation restricted when confidence is low |
| NORMAL | standard explanation generation |
| VERBOSE | extended reasoning output |

SAFE mode prevents the system from presenting potentially unreliable explanations.

**Human-in-the-Loop Override**

Clinicians can override model predictions and provide justification.

Override actions are logged for auditability.

---

## 7. Future Monitoring Strategy

Future production deployments should incorporate automated monitoring.

Recommended mechanisms include:

**Drift Detection**

- Population Stability Index (PSI)
- feature distribution monitoring

**Calibration Monitoring**

- probability calibration tracking
- reliability curve monitoring

**Continuous Evaluation**

- periodic performance audits
- model retraining when drift is detected

These strategies ensure that model performance remains stable as clinical data evolves.

---

## Summary

Distribution shift represents a significant challenge in clinical AI systems.

Although the CKD prediction model shows strong performance on the training distribution, robustness testing indicates sensitivity to input perturbations.

The system therefore incorporates:

- confidence-based decision control
- reasoning safety guardrails
- human oversight mechanisms

These safeguards help maintain reliability in real-world usage.