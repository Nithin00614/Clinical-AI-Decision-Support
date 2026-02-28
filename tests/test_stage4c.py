from genai.evaluation.evaluate_faithfulness import evaluate_faithfulness
from genai.evaluation.evaluate_grounding import evaluate_grounding
from genai.retrieval.test_retrieval import search  

# real SHAP output 
shap_features = {
    "serum_creatinine": 0.34,
    "hemoglobin": 0.21,
    "blood_urea": 0.15
}

# Real retrieval using FAISS
query = "serum creatinine hemoglobin CKD risk"
retrieved_chunks = search(query, k=3)

# Stage 4C evaluations
faithfulness = evaluate_faithfulness(shap_features, retrieved_chunks)
grounding = evaluate_grounding(retrieved_chunks)

print("Stage 4C — Faithfulness:", faithfulness)
print("Stage 4C — Grounding:", grounding)
