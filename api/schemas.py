from pydantic import BaseModel, Field, ConfigDict

class PatientInput(BaseModel):
    model_config = ConfigDict(extra="forbid")  # rejects unknown fields

    bp: float = Field(...,description="Blood pressure (mmHg)")
    sg: float = Field(..., description="Specific gravity")
    al: float = Field(..., description="Albumin level")
    su: float = Field(..., description="Sugar level")
    rbc: float = Field(...,ge=0,le=1,description="Red blood cells indicator")
    bu: float = Field(..., description="Blood urea")
    sc: float = Field(..., description="Serum creatinine")
    sod: float = Field(..., description="Sodium level")
    pot: float = Field(..., description="Potassium level")
    hemo: float = Field(..., description="Hemoglobin level")
    wbcc: float = Field(..., description="White blood cell count")
    rbcc: float = Field(..., description="Red blood cell count")
    htn: float = Field(..., description="Hypertension indicator")
