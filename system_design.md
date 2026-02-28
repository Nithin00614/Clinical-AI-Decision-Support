
Clinical AI System – System Design

1. Objective

Design an end-to-end EHR-integrated AI system for Chronic Kidney Disease (CKD) risk prediction with:

Calibrated predictive modeling

SHAP-based explainability

Clinical reasoning layer (LLM-assisted)

Retrieval-Augmented Generation (RAG)

Output guardrails

Audit logging


The system prioritizes clinical trust, modularity, and extensibility.


---

2. High-Level Architecture

Client (UI)
   │
   ▼
FastAPI API Layer
   │
   ▼
Orchestrator Service
   │
   ├── Inference Service (Logistic Model)
   ├── Confidence Calibration Service
   ├── SHAP Explainability Layer
   ├── Reasoning Service (LLM)
   ├── Retrieval Adapter (Guidelines RAG)
   └── Output Guardrails


---

3. Request Flow

1. User submits patient clinical parameters.


2. API validates request using schema layer.


3. Orchestrator triggers:

Prediction (Logistic Regression pipeline)

Probability calibration

SHAP explanation generation

Retrieval of clinical guidelines

LLM-based structured reasoning



4. Guardrails validate output consistency.


5. Final structured response returned to UI.




---

4. Core Components

4.1 Inference Layer

Pre-trained Logistic Regression model

Feature-aligned preprocessing pipeline

Calibrated probabilities

Binary risk classification


4.2 Confidence Calibration

Sigmoid/Platt scaling applied post prediction

Prevents overconfident probabilities

Improves reliability in moderate-risk cases


4.3 Explainability Layer

SHAP-based local explanations

Top feature contributors

Clinical translation layer


4.4 Reasoning Layer

Structured LLM prompt

SHAP-aware explanation

Retrieved guideline grounding

Latency tracking


4.5 Retrieval-Augmented Generation (RAG)

Indexed CKD guidelines

Context injection into reasoning prompt

Grounded explanation generation


4.6 Guardrails

Output validation

Contradiction detection

Safe formatting enforcement



---

5. Data Flow

Raw Input
→ Feature Alignment
→ Model Prediction
→ Calibration
→ SHAP Computation
→ Retrieval Context
→ LLM Reasoning
→ Guardrail Validation
→ Final JSON Response


---

6. Modularity Design Choices

Separation of inference and reasoning layers

Dedicated confidence service

Independent SHAP loader

Orchestrator controls flow

Services loosely coupled via function contracts


This ensures:

Maintainability

Replaceable model architecture

Extensible reasoning layer

Future microservice decomposition



---

7. Production Readiness Considerations

Docker containerization

Model artifact loading at startup

Environment variable configuration

Audit logging (hitl_audit_log.jsonl)

Drift monitoring artifacts

Calibration metrics tracking



---

8. Scalability Strategy (Future)

Model server isolation

Separate LLM microservice

Async processing for reasoning

Redis-based caching for retrieval

Horizontal scaling via container orchestration



---

9. Security Considerations

Input validation via schema layer

Output guardrails

API key protection for LLM

Logging without PHI persistence



---

10. Why Logistic Regression?

Clinical interpretability

Linear contribution transparency

SHAP consistency

Lower overfitting risk

Regulatory friendliness



---

11. Trade-Offs

Choice	Benefit	Trade-off

Logistic Model	Interpretable	Limited non-linear modeling
RAG Layer	Grounded explanation	Slight latency increase
Modular Services	Clean architecture	More components to manage



---

12. Future Enhancements

Multi-model ensemble

Temporal EHR modeling

Advanced calibration methods

Deployment monitoring dashboard

CI/CD integration

