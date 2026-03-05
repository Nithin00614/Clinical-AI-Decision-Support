# tests/test_llm_hallucination.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genai.llm.run_llm_reasoning import run_llm_stage


def test_grounded_explanation():
    """
    Test normal grounded reasoning when evidence + SHAP drivers exist
    """

    stage4_payload = {
        "risk_score": 0.78,
        "confidence": 0.64,
        "decision_mode": "VERBOSE",
        "model_version": "ckd_v1",

        # SHAP information
        "shap": {
            "top_positive": [
                {"feature": "blood pressure", "impact": 1.2},
                {"feature": "hemoglobin", "impact": -0.9}
            ],
            "top_negative": [],
            "vector_available": True
        },

        # Evidence retrieved
        "retrieved_evidence": [
            "Hypertension is a major risk factor for chronic kidney disease progression.",
            "Low hemoglobin levels are associated with CKD due to reduced erythropoietin production."
        ],

        "retrieval_failed": False
    }

    result = run_llm_stage(stage4_payload)

    print("Drivers:", result["reasoning_metadata"]["shap_used"])
    print("Evidence used:", result["reasoning_metadata"]["evidence_used"])

    print("\n===== TEST 1 : GROUNDED EXPLANATION =====")
    print("Clinician Summary:\n", result["clinician_summary"])
    print("\nFull Explanation:\n", result["full_explanation"])
    print("\nMetadata:\n", result["reasoning_metadata"])



def test_no_evidence_safety():
    """
    Test hallucination resistance when evidence is missing
    """

    stage4_payload = {
        "risk_score": 0.78,
        "confidence": 0.64,
        "decision_mode": "SAFE",
        "model_version": "ckd_v1",

        # SHAP information
        "shap": {
            "top_positive": [
                {"feature": "blood pressure", "impact": 1.2},
                {"feature": "hemoglobin", "impact": -0.9}
            ],
            "top_negative": [],
            "vector_available": True
        },

        # No evidence retrieved
        "retrieved_evidence": [],

        "retrieval_failed": True
    }

    result = run_llm_stage(stage4_payload)

    print("\n===== TEST 2 : NO EVIDENCE SAFETY =====")
    print("Clinician Summary:\n", result["clinician_summary"])
    print("\nFull Explanation:\n", result["full_explanation"])
    print("\nMetadata:\n", result["reasoning_metadata"])

def test_wrong_medical_evidence():

    stage4_payload = {
        "risk_score": 0.78,
        "confidence": 0.64,
        "decision_mode": "VERBOSE",

        "shap_explanation": "Blood pressure and hemoglobin influence CKD risk.",

        # intentionally wrong evidence
        "retrieved_evidence": [
            "Asthma is a chronic inflammatory disease of the lungs."
        ],

        "retrieval_failed": False
    }

    result = run_llm_stage(stage4_payload)

    print("\n===== HALLUCINATION STRESS TEST =====")
    print(result["full_explanation"])

if __name__ == "__main__":
    test_grounded_explanation()
    test_no_evidence_safety()
    test_wrong_medical_evidence()