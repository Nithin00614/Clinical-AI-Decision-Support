from pydantic import BaseModel, Field, ConfigDict

from pydantic import BaseModel, Field

class PatientInput(BaseModel):
    class Config:
        title = "CKD Patient Clinical Input"

    bp: float = Field(..., ge=40, le=300, description="Blood pressure (mmHg)", example=120)
    sg: float = Field(..., ge=1.0, le=1.05, description="Specific gravity of urine", example=1.02)
    al: float = Field(..., ge=0, le=5, description="Albumin level", example=1)
    su: float = Field(..., ge=0, le=5, description="Sugar level", example=0)

    rbc: int = Field(..., ge=0, le=1, description="Red blood cells abnormality (0=no, 1=yes)", example=1)

    bu: float = Field(..., ge=0, le=300, description="Blood urea (mg/dL)", example=36)
    sc: float = Field(..., ge=0, le=20, description="Serum creatinine (mg/dL)", example=1.2)

    sod: float = Field(..., ge=100, le=180, description="Sodium level (mEq/L)", example=137)
    pot: float = Field(..., ge=1, le=10, description="Potassium level (mEq/L)", example=4.5)

    hemo: float = Field(..., ge=0, le=25, description="Hemoglobin (g/dL)", example=15.4)
    wbcc: float = Field(..., ge=0, le=30000, description="White blood cell count", example=7800)
    rbcc: float = Field(..., ge=0, le=10, description="Red blood cell count", example=5.2)

    htn: int = Field(..., ge=0, le=1, description="Hypertension indicator (0=no, 1=yes)", example=1)
