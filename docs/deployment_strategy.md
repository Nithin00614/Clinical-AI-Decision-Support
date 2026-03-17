# Deployment Strategy (Design-Level)

## Overview

This system is designed for modular deployment but is currently implemented as a local pipeline due to compute constraints.

---

## 1. Architecture Style

- Modular service-oriented design
- Each layer can be independently deployed:
  - ML Inference Service
  - SHAP Explanation Service
  - Retrieval Service
  - LLM Reasoning Service
  - Guardrails & Validation Layer

---

## 2. Suggested Deployment Stack

- Backend: FastAPI
- Model Serving: Local / REST API
- LLM: API-based (e.g., Groq/OpenAI)
- Vector DB: FAISS / Pinecone (optional)
- Frontend: Streamlit / React

---

## 3. Pipeline Deployment Flow

User Input → API Gateway →  
ML Service → SHAP Service →  
Retrieval Service →  
LLM Reasoning →  
Guardrails →  
Response

---

## 4. Safety Layer Deployment

- Confidence calibration runs before LLM
- Guardrails applied after LLM
- Reasoning validation runs before final output

---

## 5. Human-in-the-Loop (HITL)

- Clinician override API endpoint
- Override stored and logged
- Decision source tracked (MODEL vs CLINICIAN)

---

## 6. Observability (Planned)

- Log:
  - risk score
  - confidence
  - decision mode
  - explanation reliability
- Track:
  - LLM latency
  - retrieval success
  - SHAP availability

---

## 7. Limitations

- Not deployed due to hardware constraints
- No real-time monitoring pipeline
- No distributed scaling

---

## 8. Future Improvements

- Docker containerization
- Cloud deployment (AWS/GCP)
- Real-time monitoring dashboards
- CI/CD pipeline


---