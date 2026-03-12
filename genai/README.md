# GenAI Reasoning Layer

## 1. Purpose of the GenAI Layer

The GenAI layer provides **structured clinical reasoning** on top of the machine learning prediction.

While the predictive model estimates CKD risk probability, the reasoning layer translates model outputs into **clinically interpretable explanations**.

Its goals are to:

- translate model outputs into human-readable clinical reasoning
- ground explanations using clinical guideline evidence
- prevent unsupported claims through safety guardrails
- improve interpretability for clinicians

This layer operates as a **reasoning component**, not a diagnostic system.

---

## 2. Role in the System Pipeline

The reasoning layer sits after model prediction and explainability.

Pipeline flow:

```
Model Prediction
↓
SHAP Feature Attribution
↓
Evidence Retrieval
↓
Evidence Filtering
↓
LLM Clinical Reasoning
↓
Output Guardrail Validation
↓
Structured Explanation
```

This design ensures explanations are **grounded in model signals and clinical evidence**.

---

## 3. Inputs to the Reasoning Engine

The reasoning engine receives structured inputs from earlier pipeline stages.

Key inputs include:

- predicted CKD risk probability
- risk category label
- SHAP feature attribution drivers
- retrieved clinical guideline evidence
- reasoning constraints and formatting rules

These inputs ensure the LLM produces **controlled, grounded explanations rather than free-form text generation**.

---

## 4. Prompt Design Strategy

The reasoning engine uses a **structured prompt design** to reduce hallucinations and enforce explanation consistency.

Key prompt design principles include:

- strict reliance on SHAP feature drivers
- restriction against introducing new clinical risk factors
- use of retrieved guideline evidence for grounding
- structured output format for predictable explanations
- explicit uncertainty statements when evidence is limited

This design ensures explanations remain **aligned with model behavior and available evidence**.

---

## 5. Evidence Retrieval (RAG)

The system uses a **Retrieval-Augmented Generation (RAG)** approach to ground reasoning.

Evidence retrieval:

- searches an indexed clinical knowledge base
- retrieves guideline excerpts relevant to the identified risk drivers
- injects supporting evidence into the reasoning prompt

Example sources include:

- CKD clinical guideline excerpts
- nephrology reference materials

This grounding mechanism helps reduce hallucination risk and improves clinical interpretability.

---

## 6. Guardrails and Safety Controls

Multiple safeguards are implemented to ensure reliable reasoning.

These include:

- **Feature grounding:** explanations must reference SHAP drivers
- **Evidence filtering:** only relevant evidence is used
- **Output structure enforcement:** reasoning must follow predefined sections
- **SAFE decision mode:** reasoning may be restricted when prediction confidence is low

These controls prevent unsupported claims and improve reasoning reliability.

---

## 7. Reasoning Traceability

The system records execution trace metadata for the reasoning pipeline.

Trace stages include:

```
Prediction
↓
SHAP Attribution
↓
Evidence Retrieval
↓
Evidence Filtering
↓
LLM Explanation Generation
↓
Guardrail Validation
↓
Reliability Diagnostics
```

This traceability allows the system to expose reasoning transparency and helps diagnose failures during development.

---

## 8. Known Limitations

The reasoning layer has several limitations:

- explanations depend on the quality of retrieved evidence
- reasoning may be limited when evidence retrieval fails
- outputs are constrained to the available SHAP feature drivers
- the system does not provide clinical diagnosis

The reasoning layer should therefore be interpreted as **AI-assisted explanation support**.

---

## 9. Future Improvements

Potential improvements for future versions include:

- improved clinical evidence retrieval coverage
- structured reasoning graphs for explanation validation
- hallucination detection mechanisms
- reasoning consistency evaluation

These improvements would further strengthen the reliability of the reasoning system.