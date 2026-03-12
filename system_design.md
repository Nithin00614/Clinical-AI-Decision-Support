# System Design – CKD AI Clinical Decision Support System

## 1. System Objective

Design an **AI-powered clinical decision support system** for **Chronic Kidney Disease (CKD) risk prediction** integrating:

- Machine Learning Risk Prediction
- SHAP Explainability
- Clinical Evidence Retrieval (RAG)
- LLM-Assisted Clinical Reasoning
- Output Safety Guardrails
- Human-in-the-Loop Audit Logging

The system prioritizes:

- Clinical interpretability
- Safety-aware reasoning
- Transparent decision support
- Modular architecture

The system acts as **decision support only — final clinical decisions remain with clinicians.**

---

## 2. High-Level Architecture

The system follows a layered architecture:

```
Client UI
   │
   ▼
FastAPI API Layer
   │
   ▼
Decision Orchestrator
   │
   ├── Risk Prediction Engine
   ├── Confidence Calibration
   ├── SHAP Explainability
   ├── Evidence Retrieval (RAG)
   ├── LLM Clinical Reasoning
   └── Output Guardrails
```

### Architecture Layers

**Presentation Layer**
- Streamlit clinical dashboard
- reasoning trace visualization
- clinician override interface

**API Layer**
- request validation
- schema enforcement
- routing to orchestrator

**Clinical Intelligence Layer**
- model inference
- explainability
- evidence retrieval
- reasoning generation
- guardrail validation

**Data & Knowledge Layer**

- trained ML model artifacts  
- SHAP explanation artifacts  
- clinical guideline knowledge base  
- audit logs  

---

## 3. End-to-End Inference Pipeline

Each prediction request flows through the following pipeline:

```
Patient Input
↓
API Validation
↓
Risk Prediction Model
↓
Probability Calibration
↓
SHAP Explainability
↓
Clinical Evidence Retrieval
↓
LLM Reasoning Generation
↓
Output Guardrails
↓
Confidence & Reliability Assessment
↓
Structured Response to UI
```

Each stage produces **metadata used for traceability and system diagnostics**.

---

## 4. Core System Components

### Risk Prediction Engine

- Logistic Regression model trained for CKD risk classification
- Feature-aligned preprocessing pipeline

Outputs:

- risk probability
- binary risk prediction

Logistic regression is chosen for **interpretability and clinical transparency**.

---

### Confidence Calibration

Probability calibration improves prediction reliability.

Method used:

- Sigmoid / Platt scaling

Benefits:

- reduces overconfident predictions
- improves reliability in moderate-risk cases

---

### Explainability Layer

Uses **SHAP (SHapley Additive Explanations)** for local interpretability.

Provides:

- feature contribution scores
- dominant clinical risk drivers
- interpretable explanation signals

This allows clinicians to understand **why a prediction was generated**.

---

### Evidence Retrieval (RAG)

Retrieval-Augmented Generation integrates clinical knowledge sources.

Capabilities:

- retrieval of CKD guideline excerpts
- contextual evidence injection
- evidence-grounded explanation generation

This improves reasoning reliability and reduces hallucination risk.

---

### Clinical Reasoning Engine

The reasoning layer synthesizes:

- model prediction
- SHAP feature drivers
- retrieved clinical evidence

A structured LLM prompt generates:

- clinician-friendly explanations
- risk interpretation summaries
- evidence-grounded reasoning

Reasoning latency and metadata are recorded for monitoring.

---

### Output Guardrails

Guardrails enforce safety constraints on generated explanations.

Responsibilities include:

- preventing unsupported medical claims
- validating reasoning consistency
- restricting explanations in low-confidence cases
- enforcing structured response formatting

Guardrails operate **after reasoning generation**.

---

## 5. Confidence & Decision Modes

The system distinguishes between **prediction probability** and **reasoning reliability**.

Three reasoning modes are supported:

| Mode | Behavior |
|------|----------|
| SAFE | reasoning restricted due to low confidence |
| NORMAL | standard explanation output |
| VERBOSE | detailed reasoning with full evidence |

SAFE mode prevents potentially unreliable explanations from being shown.

---

## 6. Human-in-the-Loop Workflow

Clinicians remain the **final decision authority**.

The system supports:

- clinician override of AI predictions
- documentation of override justification
- audit logging of override events

Override logs are stored in:

```
hitl_audit_log.jsonl
```

This ensures **traceability and accountability**.

---

## 7. Observability & Monitoring

Operational diagnostics improve system transparency.

Metrics include:

- reasoning pipeline traceability
- component execution status
- inference latency metrics
- reliability diagnostics

These signals support monitoring and debugging.

---

## 8. Failure Modes & Mitigation

| Failure Scenario | Mitigation |
|------------------|------------|
| Low model confidence | SAFE reasoning mode |
| Evidence retrieval failure | fallback reasoning generation |
| Explainability unavailable | degraded explanation mode |
| LLM instability | guardrail validation |
| Output inconsistency | guardrail rejection |

The system is designed to **degrade gracefully rather than fail completely**.

---

## 9. Security Considerations

Security mechanisms include:

- strict API input validation
- output guardrail enforcement
- protected LLM API access
- audit logging without storing sensitive patient identifiers

These measures ensure safe system operation.

---

## 10. Key Design Trade-offs

| Design Choice | Benefit | Trade-off |
|---------------|---------|-----------|
| Logistic Regression | interpretability | limited nonlinear modeling |
| RAG reasoning | grounded explanations | increased latency |
| Modular architecture | clean system design | more components |

The system prioritizes **interpretability, transparency, and safety**.

---

## 11. Future Improvements (v2)

Potential improvements include:

Infrastructure
- asynchronous inference pipelines
- distributed retrieval services

Model Monitoring
- population stability index (PSI) drift detection
- live calibration monitoring

Reasoning Improvements
- multi-hop clinical evidence retrieval
- hallucination detection layers

Deployment
- observability dashboards
- automated CI/CD pipelines

---

## 12. Known Limitations

- trained on a limited CKD dataset
- knowledge base coverage is limited
- system has not undergone clinical validation

The system should be considered a **research prototype for AI-assisted clinical decision support**.