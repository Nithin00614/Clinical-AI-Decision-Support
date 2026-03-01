# Model Training Documentation

## Objective
Train a CKD risk prediction model using structured clinical features.

---

## Dataset

- Total samples: 400
- Features used (14):
  - Bp
  - Sg
  - Al
  - Su
  - Rbc
  - Bu
  - Sc
  - Sod
  - Pot
  - Hemo
  - Wbcc
  - Rbcc
  - Htn
- Target:
  - Class (1 = CKD, 0 = Non-CKD)

---

## Data Split Strategy

- Stratified 80–20 train-test split
- Random state fixed for reproducibility
- Test set used as final holdout cohort

---

## Model

- Algorithm: Logistic Regression
- Solver: lbfgs
- Regularization: L2
- C: 1.0
- Max iterations: 1000

Reason for Logistic Regression:
- Interpretability
- Stability
- Lower risk of overfitting on small dataset
- Clinically explainable coefficients

---

## Pipeline Components

- Missing value handling
- Feature scaling
- Categorical encoding
- Probability calibration

Final artifact:

models/full_pipeline.pkl

---

## Observations

- Dataset highly separable
- Logistic regression achieved near-perfect separation
- Calibration improved probability stability


## Model Selection Rationale

Logistic Regression was selected over tree-based or deep learning models because:
Dataset size is small (400 samples)
High interpretability required for clinical setting
Linear separability observed during EDA
Lower overfitting risk compared to complex models
Coefficients are clinically interpretable

-Alternative models considered:

Random Forest (higher complexity, reduced interpretability)
Gradient Boosting (risk of overfitting small dataset)
Neural Networks (not suitable for small tabular dataset)
Given dataset characteristics, logistic regression provided optimal balance between performance and interpretability.