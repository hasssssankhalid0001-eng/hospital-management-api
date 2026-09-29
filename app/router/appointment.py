from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.util.database import get_db
from app.model.appointment import Appointment
from app.model.patient import Patient
from app.model.doctor import Doctor
from app.schema.appointment import (
    AppointmentCreate,
    AppointmentUpdate
)
from app.util.auth import require_admin

from fastapi import APIRouter, Depends
from app.util.auth import require_admin

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
    dependencies=[Depends(require_admin)]
)


@router.post("/appointment")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        reason=appointment.reason,
        status=appointment.status
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/appointments")
def get_all_appointments(
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).all()

    return appointments


@router.get("/appointment/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


@router.get("/patient/{patient_id}/appointments")
def get_patient_appointments(
    patient_id: str,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient.appointments


@router.get("/doctor/{doctor_id}/appointments")
def get_doctor_appointments(
    doctor_id: str,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor.appointments


@router.put("/appointment/{appointment_id}")
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    updated_data = appointment_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)

    return appointment


@router.delete("/appointment/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }