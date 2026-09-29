from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.util.database import get_db
from app.model.medical_record import MedicalRecord
from app.model.patient import Patient
from app.model.doctor import Doctor
from app.schema.medical_record import (MedicalRecordCreate,MedicalRecordUpdate)
from app.util.auth import require_admin

router = APIRouter(

    prefix="/medical-records",

    tags=["Medical Records"],

    dependencies=[Depends(require_admin)]

)

@router.post("/medical-record")
def create_medical_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == record.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == record.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_record = MedicalRecord(
        patient_id=record.patient_id,
        doctor_id=record.doctor_id,
        diagnosis=record.diagnosis,
        treatment=record.treatment
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.get("/medical-record/{record_id}")
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    return record  


@router.get("/patient/{patient_id}/medical-records")
def get_patient_records(
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

    return patient.records

@router.put("/medical-record/{record_id}")
def update_medical_record(
    record_id: int,
    record_update: MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    updated_data = record_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record

@router.delete("/medical-record/{record_id}")
def delete_medical_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Medical record deleted successfully"
    }