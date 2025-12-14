

 1️⃣ Project Title

*Multimodal Clinical Decision Support System for Chronic Kidney Disease*



 2️⃣ Problem Statement

Chronic Kidney Disease (CKD) is a progressive condition that often remains undiagnosed until advanced stages, leading to severe health complications and increased mortality. Early detection of CKD enables timely intervention and can significantly slow disease progression. This project aims to develop an AI-based clinical decision support system that predicts the presence of CKD using structured clinical and laboratory data. The system emphasizes accurate and explainable predictions to support clinicians in early risk assessment.



3️⃣ Motivation & Importance

* CKD affects millions worldwide and is a major public health concern
* Late diagnosis leads to irreversible kidney damage
* Manual assessment of multiple clinical indicators is time-consuming
* AI can assist clinicians by identifying hidden patterns in patient data
* Explainable AI is essential for trust in medical decision-making

---

4️⃣ AI Task Definition

* **Problem Type:** Binary Classification
* **Learning Type:** Supervised Learning
* **Input Data:** Structured tabular clinical data
* **Output:** CKD / Not CKD prediction
* **Domain:** Healthcare / Medical AI

---
 5️⃣ Dataset Description


- Dataset Name: Chronic Kidney Disease Dataset
- Source: UCI Machine Learning Repository
- Number of Samples: ~400
- Number of Features: 14 clinically relevant attributes + target label
- Data Type: Structured tabular clinical data


---

 6️⃣ Input & Output Specification

 Inputs

* Patient demographics (age, blood pressure)
* Laboratory test results (serum creatinine, hemoglobin, albumin, glucose)

 Output

* Binary prediction indicating CKD presence
* Model confidence score (later extension)

---

7️⃣ Evaluation Metrics

* **Recall (Primary):** Missing a CKD patient can have serious consequences
* **Precision:** Avoid unnecessary false alarms
* **ROC-AUC:** Measures overall discriminative ability
* **Accuracy:** Supporting metric


8️⃣ Data Quality Considerations

* Presence of missing values in several features
* Missing values represented as `?` in the dataset
* Potential class imbalance between CKD and non-CKD samples
* Inconsistent data types (numerical values stored as strings)


9️⃣ Ethical Considerations & Limitations

* Dataset may not represent all populations
* Model predictions are for research purposes only
* False negatives are clinically risky
* Model must be explainable to be trusted
* Not intended for real-world clinical deployment



1️⃣0️⃣ High-Level System Architecture (Conceptual)

```
Raw Clinical Data
        ↓
Data Preprocessing
        ↓
ML / DL Prediction Model
        ↓
Explainability (SHAP)
        ↓
Clinical Decision Support Output

1️⃣1️⃣ Future Extensions (Brief)

* Integrate clinical text using NLP
* Add medical knowledge via RAG and LLMs
* Extend to multimodal data (images, time-series)
* Deploy as a web-based clinical dashboard

-
### Target Variable
- Column name: Class
- Task type: Binary classification
- Class labels:
  - 1 → Chronic Kidney Disease (CKD)
  - 0 → Not CKD

### Input Features
The remaining columns (Bp, Sg, Al, Su, Bu, Sc, Hemo, etc.) represent clinical and laboratory measurements used as input features for prediction.
Note:
- Input features are the variables used for prediction (Bp, Bu, Sc, Hemo, etc.)
- The target variable is 'Class'
- Class labels are the values of 'Class' (0 = Not CKD, 1 = CKD)


### Missing Value Check
- All columns contain zero missing values as confirmed using `isnull().sum()`.
- No placeholder symbols or NaN values were detected.
- The dataset is technically clean and suitable for direct modeling.

### Target Distribution Analysis
- CKD cases constitute approximately 62.5% of the dataset.
- Non-CKD cases constitute approximately 37.5%.
- The dataset shows moderate class imbalance.
- In a clinical setting, false negatives (missed CKD cases) are more dangerous than false positives.
- Therefore, recall for the CKD class is prioritized during model evaluation.

### Feature Categorization
- Target variable: Class
- Binary clinical indicators: treated as categorical (not scaled)
- Continuous laboratory measurements: standardized using scaling
- Rationale: preserve clinical meaning while ensuring numerical stability

### Data Splitting Strategy
- Stratified train-test split is used to preserve class distribution
- Prevents biased evaluation due to class imbalance

-Scaling ensures numerical features are on comparable ranges so models train correctly and fairly.
-Stratification ensures class proportions are preserved across train and test splits, preventing biased evaluation, especially in imbalanced medical datasets

### Baseline Model Observations
- Logistic Regression used as an interpretable baseline
- Stratified split preserved CKD distribution
- Recall for CKD class is prioritized over accuracy
- ROC-AUC used to assess ranking quality

### Risk Score Interpretation
- Model outputs a probability representing CKD risk
- Higher probability indicates higher clinical risk
- Enables threshold-based decision support instead of binary prediction

### Error & Uncertainty Analysis
- False negatives are clinically most critical
- Low-confidence predictions highlight cases requiring further testing
- Risk-based outputs allow safer decision-making than hard labels

### Uncertainty-Aware Risk Estimation
Instead of relying solely on binary predictions, the model outputs a probability score representing CKD risk. Predictions closer to 0.5 are treated as low-confidence, while extreme values indicate higher confidence. This approach supports safer clinical decision-making by identifying uncertain cases that may require additional testing.

### Threshold Optimization
The default 0.5 threshold was adjusted to prioritize recall for CKD cases. Lower thresholds increase sensitivity and reduce the risk of missed diagnoses, which is critical in clinical screening scenarios. Threshold selection was guided by recall–precision trade-offs rather than accuracy alone.

### Explainability with SHAP
SHAP was used to provide global and local explanations for CKD risk predictions. Global explanations identified clinically relevant features such as serum creatinine and hemoglobin as key drivers. Local explanations enabled patient-level transparency by highlighting individual risk contributors.

“I used SHAP to provide both global and patient-level explanations. SHAP decomposes the model’s predicted CKD risk into additive feature contributions, allowing me to identify clinically meaningful drivers such as serum creatinine and hemoglobin. This ensures transparency and trust in medical decision support."

### Counterfactual Analysis
Counterfactual reasoning was used to evaluate how minimal, clinically plausible changes in laboratory values affect CKD risk. Simulated improvements in serum creatinine and hemoglobin resulted in a reduced predicted risk, demonstrating actionable decision support rather than static prediction.

### Model Comparison
Logistic Regression was used as an interpretable baseline, while XGBoost was introduced to capture non-linear feature interactions. Performance was compared using identical preprocessing, stratified splits, and clinically motivated thresholds to ensure fair evaluation.

### Model-Level Uncertainty
Uncertainty was estimated using disagreement between Logistic Regression and XGBoost predictions. Cases with high disagreement were flagged as uncertain, highlighting scenarios where additional clinical validation may be required.

“I compared interpretable and non-linear models under a consistent pipeline and used ensemble disagreement to estimate uncertainty instead of blindly trusting a single model."

### Knowledge Base
A small, curated medical knowledge base was created using trusted CKD guideline excerpts to support grounded clinical reasoning and prevent hallucinated explanations.

### Retrieval-Augmented Reasoning
Relevant CKD guidelines were retrieved based on SHAP-identified risk factors and provided as grounded context for clinical reasoning, ensuring explanations remain evidence-based.

##Prompt template.
You are a clinical decision support assistant.
Use ONLY the provided medical guidelines.
Explain why the patient is at risk and suggest next clinical steps.
Do not provide diagnoses or treatment.

“I integrated a retrieval-augmented LLM layer that grounds model predictions and SHAP explanations in trusted medical guidelines, preventing hallucinations and enabling transparent clinical reasoning.”

## System Summary
This project implements an uncertainty-aware, explainable, and retrieval-augmented clinical decision support system for CKD risk assessment, combining machine learning, interpretability, counterfactual analysis, and grounded LLM reasoning.
