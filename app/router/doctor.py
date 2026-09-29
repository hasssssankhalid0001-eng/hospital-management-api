from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.util.database import get_db
from app.model.doctor import Doctor
from app.schema.doctor import DoctorCreate, DoctorUpdate

from app.util.auth import require_admin

router = APIRouter(

    prefix="/doctors",

    tags=["Doctors"],

    dependencies=[Depends(require_admin)]

)


@router.post("/doctor")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    new_doctor = Doctor(
        id=doctor.id,
        name=doctor.name,
        specialization=doctor.specialization,
        department=doctor.department,
        experience=doctor.experience,
        email=doctor.email
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@router.get("/doctors")
def get_all_doctors(
    db: Session = Depends(get_db)
):
    doctors = db.query(Doctor).all()

    return doctors


@router.get("/doctor/{doctor_id}")
def get_doctor(
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

    return doctor


@router.put("/doctor/{doctor_id}")
def update_doctor(
    doctor_id: str,
    doctor_update: DoctorUpdate,
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

    updated_data = doctor_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor


@router.delete("/doctor/{doctor_id}")
def delete_doctor(
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

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }

@router.get("/doctor/{doctor_id}/medical-records")
def get_doctor_records(
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

    return doctor.records