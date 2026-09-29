from pydantic import BaseModel
from typing import Optional


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: str
    reason: str
    status: str


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None