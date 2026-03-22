# Model Card – CKD Risk Prediction Model

## 1. Model Overview

This model predicts the probability of **Chronic Kidney Disease (CKD)** using structured clinical indicators.

The model is designed as a component within a **clinical decision-support system** that integrates prediction, explainability, and reasoning layers.

Key characteristics:

- **Model Type:** Logistic Regression (Calibrated)
- **Prediction Task:** Binary CKD risk classification
- **Input Type:** Structured clinical features
- **Output:** CKD risk probability (0–1)

The model prioritizes **interpretability and clinical transparency**.

---

## 2. Model Architecture

The prediction pipeline consists of:

1. Feature preprocessing pipeline
2. Logistic Regression classifier
3. Probability calibration layer
4. SHAP-based explainability module

Pipeline flow:

```
Clinical Input Features
↓
Feature Alignment & Preprocessing
↓
Logistic Regression Prediction
↓
Probability Calibration
↓
SHAP Feature Attribution
```

Logistic Regression was selected due to:

- interpretability
- stable feature contributions
- compatibility with SHAP explanations
- lower overfitting risk for small datasets

---

## 3. Training Data

The model was trained using a structured CKD dataset containing clinical indicators.

**Dataset characteristics**

- Dataset Size: 400 patient records
- Feature Count: 13 structured clinical indicators
- Feature Type: Numeric and categorical clinical measurements

Examples of input features:

- Blood Pressure
- Specific Gravity
- Albumin
- Blood Urea
- Serum Creatinine
- Hemoglobin
- Sodium
- Potassium
- Red Blood Cell Count

Preprocessing includes feature alignment and normalization to ensure consistency during inference.

---

## 4. Evaluation Metrics

Model performance was evaluated using internal validation.

| Metric | Value |
|--------|-------|
| AUC | 0.9994 |
| Accuracy | 0.9825 |
| F1 Score | 0.9859 |
| Brier Score | 0.0186 |

The dataset exhibits **high linear separability**, making logistic regression an effective baseline model.

---

## 5. Explainability Strategy

The model incorporates **SHAP-based explainability** to provide transparent feature attribution.

Explainability outputs include:

- top risk-increasing clinical drivers
- protective feature contributions
- structured feature importance rankings

These explanations enable clinicians to understand **which features influenced the prediction**.

In the complete system pipeline, SHAP explanations are combined with:

- clinical evidence retrieval
- structured LLM reasoning
- safety guardrails

to produce interpretable clinical explanations.

---

## 6. Confidence System

The system distinguishes between **prediction probability** and **prediction reliability**.

Confidence scoring incorporates:

- model certainty (distance from decision boundary)
- SHAP explanation availability
- presence of supporting clinical evidence

Confidence is used to control system behavior through **decision modes**:

| Mode | Description |
|------|-------------|
SAFE | explanation restricted due to low confidence |
NORMAL | standard reasoning output |
VERBOSE | extended reasoning transparency |

Confidence is **not equivalent to probability**.

---

## 7. Robustness Findings

Robustness testing was conducted using Gaussian noise perturbation.

Observed effect:

| Metric | Baseline | Under Noise |
|--------|----------|-------------|
| AUC | 0.9994 | 0.6629 |

This indicates sensitivity to **distribution shift**.

Mitigation strategies implemented in the system include:

- confidence-based decision control
- human-in-the-loop override
- reasoning guardrails

---

## 8. Model Limitations

The model has several limitations:

- trained on a relatively small dataset
- limited demographic diversity
- not externally validated on multiple clinical populations
- may be sensitive to distribution shifts

"External validation was attempted but not completed due to limited availability of sufficiently diverse and clean public CKD datasets. A held-out hospital cohort would be required for production validation."

Predictions should therefore be interpreted as **decision-support signals rather than diagnostic conclusions**.

---

## 9. Ethical and Safety Considerations

This system is designed for **clinical decision support only**.

The model:

- does **not replace physician judgment**
- does **not provide treatment recommendations**
- should be used with **clinical oversight**

Human review is required for real-world deployment.

---

## 10. Monitoring Strategy

For production deployment, monitoring mechanisms should include:

- data drift detection
- calibration monitoring
- periodic model retraining
- reasoning reliability tracking

These mechanisms ensure model performance remains stable over time.

---

## 11. Model Version

```
Model Version: CKD-Predictor-v1.0
Training Dataset Version: CKD-Dataset-v1
Last Updated: 20-01-2026
```

Future versions may incorporate:

- larger datasets
- improved calibration
- external clinical validation