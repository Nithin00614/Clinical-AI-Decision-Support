from services1.inference_service import predict_patient
from services1.reasoning_service import run_reasoning

sample_input = {
    "bp": 120,
    "sg": 1.02,
    "al": 0,
    "su": 0,
    "rbc": 1,
    "bu": 10,
    "sc": 0.7,
    "sod": 140,
    "pot": 4.2,
    "hemo": 15,
    "wbcc": 7000,
    "rbcc": 5,
    "htn": 0
}


print("\nSTEP 1 — Raw Input")
print(sample_input)

print("\nSTEP 2 — Model Prediction")
pred = predict_patient(sample_input)
print(pred)

print("\nSTEP 3 — Full Reasoning Pipeline")
result = run_reasoning(sample_input)
print(result)

print("\nSTEP 4 — Final API Payload")
print(result)
