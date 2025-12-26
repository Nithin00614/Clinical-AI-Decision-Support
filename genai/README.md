# GenAI Clinical Reasoning Layer

This module extends the CKD Clinical Decision Support System by adding a
retrieval-augmented generative reasoning layer.

## Purpose
- Provide evidence-grounded explanations for ML-generated CKD risk scores
- Retrieve authoritative clinical guideline excerpts
- Translate technical model outputs into clinician-friendly reasoning

## Scope
The GenAI layer:
- Consumes ML outputs (risk score, SHAP drivers)
- Retrieves supporting evidence from clinical guidelines
- Generates grounded, explainable summaries

The GenAI layer does NOT:
- Predict CKD
- Replace the ML model
- Provide diagnoses or treatment decisions

## Design Principles
- Separation of concerns (ML predicts, GenAI explains)
- Retrieval-first reasoning (no free hallucination)
- Explicit citation of guideline sources
- Conservative response behavior when evidence is insufficient
