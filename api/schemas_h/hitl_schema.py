from pydantic import BaseModel
from typing import Optional

class ClinicianReview(BaseModel):
    patient_id: str
    model_risk_score: float
    decision_mode: str
    clinician_decision: str   # approve | override | review
    clinician_notes: Optional[str] = None
