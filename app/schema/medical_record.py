from pydantic import BaseModel
from typing import Optional


class MedicalRecordCreate(BaseModel):
    patient_id: str
    doctor_id: str
    diagnosis: str
    treatment: str


class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None