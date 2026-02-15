import json
import os

REVIEW_FILE = "hitl_audit_log.json"

def get_override(patient_id):
    if not os.path.exists(REVIEW_FILE):
        return None

    with open(REVIEW_FILE, "r") as f:
        reviews = json.load(f)

    for r in reversed(reviews):
        if r["patient_id"] == patient_id:
            return r

    return None
