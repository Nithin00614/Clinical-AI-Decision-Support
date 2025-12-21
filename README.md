
# 🩺 CKD Clinical Decision Support System

**An Explainable, Robust, and Externally Validated ML Framework**

---

## 📌 Project Overview

Chronic Kidney Disease (CKD) is a progressive condition that often remains undiagnosed until advanced stages. This project presents a **clinical decision support system (CDSS)** for CKD risk prediction using machine learning, with a strong emphasis on **interpretability, robustness, and real-world generalization**.

Unlike typical student projects that stop at model accuracy, this system evaluates:

* *Why* predictions are made (Explainability)
* *How stable* predictions are under noisy clinical data (Robustness)
* *Whether the model generalizes* to unseen populations (External Validation)

This project is designed as a **research-grade ML system** and serves as a flagship portfolio project.

---

## 🎯 Key Objectives

* Predict CKD risk using clinically relevant laboratory measurements
* Provide transparent explanations for model predictions
* Assess robustness under realistic lab measurement noise
* Validate generalization on an independent external dataset
* Follow clean, modular, and reproducible ML practices

---

## 🧠 Methodology Overview

### 1. Data Sources

* **Primary Dataset**: CKD dataset (Kaggle, derived from clinical records)
* **External Dataset**: Cleaned CKD dataset from the **UCI Machine Learning Repository**

Both datasets contain laboratory and clinical features relevant to kidney function.

---

### 2. Feature Engineering

* Focus on **numerical laboratory measurements** for stability across datasets
* Explicit separation of:

  * Numeric features
  * Binary clinical indicators
  * Categorical observations
* Processed data stored as reproducible artifacts (`data/processed/`)

---

### 3. Model Development

Two models were developed:

#### 🔹 Primary Model (Full Feature Pipeline)

* Logistic Regression with:

  * Standard scaling (numeric features)
  * One-hot encoding (categorical features)
* Used for:

  * Internal evaluation
  * Explainability analysis

#### 🔹 Secondary Model (Numeric-Only Model)

* Logistic Regression trained **only on numeric lab features**
* Purpose:

  * Enable reliable external validation
  * Avoid dataset-specific categorical encoding issues
* Used exclusively for robustness testing and cross-dataset evaluation

---

## 🔍 Explainability (SHAP)

To ensure transparency, **SHAP (SHapley Additive exPlanations)** was applied to the trained model.

* **Global explanations** identify the most influential laboratory markers
* **Local explanations** justify individual patient predictions
* SHAP analysis was performed on the trained model *after preprocessing*, ensuring faithful attribution

📌 Key Insight:
Renal biomarkers such as serum creatinine, hemoglobin, and blood urea strongly influence CKD risk predictions.

---

## 🛡️ Robustness Analysis

Clinical data is inherently noisy due to:

* Measurement variability
* Instrumentation error
* Reporting inconsistencies

To simulate this, Gaussian noise was injected into numeric features, and prediction stability was evaluated.

* Predictions remained stable under moderate noise (1–10%)
* Mean prediction shifts were limited, indicating resilience
* Both global and patient-level robustness were assessed

📌 This analysis demonstrates suitability for real-world clinical environments.

---

## 🌍 External Validation

Generalization was evaluated using an **independent CKD dataset** derived from the UCI repository.

* No retraining or tuning was performed
* Only shared numeric laboratory features were used
* Missing values (`'?'`) were safely handled to avoid leakage

### External Results Summary:

* **ROC-AUC = 1.0**
* **Zero false negatives**
* Minor false positives, favoring sensitivity over specificity

📌 Interpretation:
The model exhibits strong generalization on external data, while maintaining clinically appropriate conservative behavior.

---

## 📁 Project Structure

```
Clinical-AI-System/
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   └── ckd_processed.csv
│   └── external/
│       └── uci_ckd.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   ├── 03_explainability_shap.ipynb
│   ├── 04_robustness_analysis.ipynb
│   └── 05_external_validation.ipynb
│
├── models/
│   ├── full_pipeline.pkl
│   └── numeric_model.pkl
│
├── README.md
├── requirements.txt
└── .gitignore
```

Each notebook focuses on **one stage of the ML lifecycle**, ensuring clarity and reproducibility.

---

## 🧪 Reproducibility

1. Create a virtual environment
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run notebooks in numerical order (`01 → 05`)

All models and results can be reproduced end-to-end.

---

## 🚀 Future Work

* Integrate a **GenAI (RAG-based) reasoning layer** to:

  * Explain predictions using clinical guidelines
  * Provide evidence-backed decision support
* Extend system to medication adherence and nutrition planning
* Explore uncertainty quantification for clinical risk estimation

---

## 📌 Key Takeaways

* External validation is as important as internal accuracy
* Interpretability and robustness are critical for clinical ML systems
* Numeric laboratory features provide strong, transferable signal
* Clean project structure enhances credibility and maintainability

---

## 👤 Author

**Nithin Gowda P**
Final Year Engineering Student | Aspiring AI/ML Engineer
Focused on building **robust, explainable, and real-world ML systems**

---


