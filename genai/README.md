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

## Input Contract
- CKD risk probability (float)
- Top contributing features from SHAP analysis

## Output Contract
- Plain-language explanation of risk factors
- Evidence-backed reasoning with citations
- Clinical considerations (non-prescriptive)

## Ingestion & Chunking
Guideline PDFs are loaded page-wise and split into overlapping semantic chunks (~800 tokens, 120 overlap) to preserve clinical context while enabling precise retrieval.

## Retrieval Index
Embeddings are generated locally and stored in a FAISS index for fast cosine-similarity search. Each chunk retains source metadata (document and page).

## Retrieval Sanity Check
A standalone retrieval test validates that guideline-relevant text is returned for clinical queries (e.g., serum creatinine, CKD risk), ensuring index quality before LLM integration.
Retrieval tests confirm that clinically relevant guideline evidence (e.g., proteinuria, creatinine, albuminuria) is returned for CKD-related queries.

## Grounded Clinical Reasoning
The GenAI layer integrates ML predictions with SHAP-derived feature contributions and retrieves evidence from clinical guidelines. Reasoning is retrieval-grounded, citation-aware, and intentionally non-prescriptive.

## Stage 4A: System Faithfulness and Grounding Evaluation

We evaluate the trustworthiness of the explanation pipeline prior to LLM integration.

**Faithfulness Evaluation**
- Verifies alignment between SHAP-identified influential features and retrieved clinical guideline evidence.
- Ensures that model explanations are supported by domain-relevant medical knowledge.

**Grounding Evaluation**
- Ensures that all explanatory claims are backed by retrieved guideline text.
- When no supporting evidence is available, the system explicitly reports insufficient evidence rather than generating unsupported explanations.

This evaluation stage enforces safety, transparency, and auditability of the clinical decision support system before introducing any generative components.
