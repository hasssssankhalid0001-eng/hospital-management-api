from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schema.patient import Patient, PatientUpdate, PatientResponse 
from app.util.database import get_db
from app.model.patient import Patient as PatientModel 
from app.util.exceptions import PatientNotFoundException

from app.util.auth import require_admin

from app.model.user import User

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    dependencies=[Depends(require_admin)]
)


# Dependencies

def get_app_name():
    return "Patient Management System"


def get_patient(patient_id: str,db: Session = Depends(get_db)):

    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise PatientNotFoundException()

    return patient


def get_patient_age(patient_id: str,db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

    if not patient:
        raise PatientNotFoundException()

    return patient.age


# View all patients

@router.get('/view')
def view(db: Session = Depends(get_db),app_name=Depends(get_app_name)):
    patients = db.query(PatientModel).all()

    return {
        "app": app_name,
        "patients": patients
    }


# View one patient

@router.get('/patient/{patient_id}')
def view_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    
):
    patient = db.query(PatientModel).filter(
        PatientModel.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    return patient


# Sort patients

@router.get('/sort')
def sort_patients(sort_by: str = Query( ...,description='SORT ON THE BASIS OF HEIGHT, WEIGHT OR BMI' ),
    order: str = Query('asc',description='sort in asc OR desc'),db: Session = Depends(get_db)):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f'INVALID FIELD SELECT FROM {valid_fields}'
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail='INVALID ORDER SELECT BETWEEN asc OR desc'
        )

    if sort_by == 'bmi':
        patients = db.query(PatientModel).all()

        patients.sort(
            key=lambda patient: patient.weight / (patient.height ** 2),
            reverse=(order == 'desc')
        )

        return patients

    column = getattr(PatientModel, sort_by)

    if order == 'asc':
        patients = db.query(PatientModel).order_by(column.asc()).all()
    else:
        patients = db.query(PatientModel).order_by(column.desc()).all()

    return patients


# Create patient

@router.post('/create')
def create_patient(
    patient: Patient,
    db: Session = Depends(get_db)
):
    existing_patient = db.query(PatientModel).filter(
        PatientModel.id == patient.Pid
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail='Patient already exists'
        )

    new_patient = PatientModel(
        id=patient.Pid,
        name=patient.name,
        city=patient.city,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return JSONResponse(
        status_code=201,
        content={
            'message': 'patient created successfully'
        }
    )


# Update patient

@router.put('/edit/{Pid}')
def update_patient(
    Pid: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = db.query(PatientModel).filter(
        PatientModel.id == Pid
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    updated_data = patient_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return JSONResponse(
        status_code=200,
        content={
            'message': 'patient updated'
        }
    )


# Delete patient

@router.delete('/delete/{Pid}')
def delete_patient(
    Pid: str,
    db: Session = Depends(get_db)
):
    patient = db.query(PatientModel).filter(
        PatientModel.id == Pid
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    db.delete(patient)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={
            'message': 'patient deleted'
        }
    )


# Get patient age

@router.get("/patient-age/{patient_id}")
def patient_age(
    age=Depends(get_patient_age)
):
    return {
        "age": age
    }

@router.get("/patients")
def get_all_patients(
    db: Session = Depends(get_db)
):
    patients = db.query(PatientModel).all()

    return patients 