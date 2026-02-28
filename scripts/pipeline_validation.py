from services.inference_service import predict_patient
from services.reasoning_service import run_reasoning

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



result = run_reasoning(sample_input)
print("\n ----- FINAL PIPELINE OUTPUT ----- \n")
print(result)

