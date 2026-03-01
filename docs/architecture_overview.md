# Architecture Overview – CKD Clinical AI System


## 1️⃣ High-Level Flow

User Input  
↓  
API Layer (FastAPI)  
↓  
Inference Service  
↓  
Orchestrator  
↓  
├── Model Prediction  
├── SHAP Explainability  
├── Retrieval (Knowledge Base)  
├── Guardrails  
├── Confidence Aggregation  
↓  
Controller (Decision Mode Selection)  
↓  
Final Structured Response  

---

## 2️⃣ Core Components

### API Layer
- Handles request validation
- Uses Pydantic schemas
- Routes inference requests to services layer

---

### Inference Service
- Loads `full_pipeline.pkl`
- Applies preprocessing + calibration
- Outputs:
  - Risk probability
  - Binary prediction

---

### Orchestrator
Coordinates all reasoning layers:

- Model inference
- SHAP explanation
- Evidence retrieval
- Guardrail validation
- Confidence scoring

Ensures modular execution without tight coupling.

---

### Explainability Layer
- SHAP-based feature attribution
- Highlights dominant clinical predictors
- Enables interpretability in structured form

---

### Retrieval Layer
- Pulls structured knowledge from internal dataset
- Supports reasoning explanation
- Adds contextual support to predictions

---

### Guardrails
- Prevent unsupported claims
- Block unsafe medical recommendations
- Ensure output formatting compliance

---

### Confidence Engine

Final confidence score combines:

- Model certainty (distance from 0.5)
- SHAP explanation availability
- Retrieval evidence presence

Confidence ≠ probability.

Used for:
- Decision mode switching
- HITL activation

---

### Controller

Decision Modes:

- SAFE → Low confidence
- NORMAL → Moderate confidence
- VERBOSE → High confidence

Controls verbosity and explanation depth.

---

## 3️⃣ Data Drift Handling

Current Implementation:

- Gaussian noise robustness simulation
- Performance sensitivity testing
- Confidence-based mitigation

Future Improvements (documented):
- PSI drift monitoring
- Live calibration monitoring
- Shadow deployment validation

---

## 4️⃣ Configuration Management

`configs/config.yaml` controls:

- Model path
- Confidence weights
- Decision thresholds
- Logging level

Allows system tuning without code modification.

---

## 5️⃣ Safety Design

System incorporates:

- Human-in-the-Loop override
- Guardrails
- Confidence tagging
- Explicit limitations in model card

---

## 6️⃣ Deployment Ready Structure

- Dockerfile included
- Modular services
- Clean separation of concerns
- Production-safe logging

---

## Summary

The system is designed as a modular, safety-aware, explainable clinical AI decision-support pipeline with configurable thresholds and layered reasoning.

It prioritizes interpretability and safety over raw predictive performance.