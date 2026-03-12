# System Architecture Overview

## Overview

The **AI-Powered Clinical Decision Support System for Chronic Kidney Disease (CKD)** is designed as a layered architecture that integrates machine learning risk prediction, explainable AI, retrieval-augmented clinical evidence, and large language model reasoning.

The system analyzes patient clinical features to estimate CKD risk, generates interpretable explanations using SHAP, retrieves supporting clinical guideline evidence, and synthesizes reasoning using a language model. Safety guardrails and monitoring ensure reliability while supporting **human-in-the-loop clinical review**.

---

## System Architecture

The following diagram illustrates the high-level architecture of the system.

![System Architecture](System_architecture.png)

The system follows a **six-layer architecture** separating interface, orchestration, AI services, data infrastructure, and monitoring components.

---

# Layered Architecture

## 1. Presentation Layer

The presentation layer provides the clinician-facing interface.

Components include:

### Streamlit Clinical Dashboard
- Displays patient information
- Shows real-time CKD risk monitoring

### Prediction Interface
- Displays model risk prediction
- Shows SHAP-based feature explanations

### Clinical Reasoning Interface
- Displays evidence-grounded explanations
- Shows reasoning reliability and traceability

This layer enables clinicians to interpret AI predictions transparently.

---

## 2. API Layer

The API layer connects the user interface with backend AI services.

### FastAPI API Gateway

Responsibilities include:

- Versioned API endpoints
- Request routing to AI services

### API Gateway Functions

- Request validation
- Service routing

This layer enables modular communication between services.

---

## 3. Orchestration Layer

The orchestration layer coordinates the execution of the entire decision pipeline.

### AI Orchestration & Decision Controller

Responsibilities include:

- Pipeline execution management
- Prediction confidence evaluation
- Failure detection and fallback handling
- Decision mode control *(SAFE / NORMAL / VERBOSE)*

The controller ensures the correct execution order of all AI services.

---

## 4. AI Intelligence Layer

This layer contains the core AI services.

### CKD Risk Prediction Service

- Machine learning risk prediction model
- Clinical feature preprocessing

### SHAP Explainability Service

- SHAP feature attribution
- Feature importance ranking

### Clinical Evidence Retrieval (RAG)

- Retrieval of clinical guideline evidence
- Vector similarity search over knowledge base

### LLM Clinical Reasoning Service

- Evidence-grounded explanation generation
- SHAP-aware reasoning synthesis

### AI Safety & Guardrails

- Safety filtering
- Clinical disclaimer enforcement
- Reasoning consistency validation

---

## 5. Data & Knowledge Layer

The data layer stores models, explanations, embeddings, predictions, and logs.

### Model Registry
- Stores model artifacts and versions

### SHAP Explanation Store
- Stores precomputed SHAP values

### Vector Index
- Stores embeddings for guideline retrieval

### Clinical Knowledge Base
- Clinical guidelines such as **KDIGO / NIDDK**

### Prediction Store
- Stores prediction outputs and metadata

### Audit Log Store
- Stores clinician override logs
- Maintains decision traceability

---

## 6. Monitoring & Governance Layer

This layer ensures reliability and operational monitoring.

### Model Monitoring
- Prediction confidence tracking
- Calibration monitoring

### Data Drift Monitoring
- Input distribution shift detection
- Feature drift alerts

### System Observability
- Latency tracking
- Pipeline execution logs
- Reliability diagnostics

---

---

# Execution Flow

The system follows a structured decision pipeline:

Patient Input → Risk Prediction → SHAP Explainability → Evidence Retrieval → LLM Clinical Reasoning → Guardrail Validation → Clinician Review

The orchestration controller manages the execution of this pipeline.

---

# Design Principles

The architecture follows several key principles:

### Explainability
Every prediction includes SHAP-based explanations to ensure model transparency and interpretability.

### Evidence-Grounded Reasoning
LLM-generated reasoning is supported by retrieved clinical guideline evidence to ensure medically grounded explanations.

### Human-in-the-Loop Safety
Clinicians can review predictions and override AI-generated decisions when necessary.

### Modular Design
Each component is implemented as an independent service, enabling scalability, maintainability, and extensibility.

### Continuous Monitoring
The system tracks model performance, data drift, and operational reliability to ensure stable deployment.

---

# Additional Documentation

Detailed implementation details are documented in:

system_design.md

Additional supporting documents:

docs/model_card.md  
docs/data_shift.md

These documents describe model behavior, evaluation methodology, and robustness considerations.