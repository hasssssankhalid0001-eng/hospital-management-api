import time
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from app.router import patient
from app.router import medical_record
from app.router import doctor
from app.router import staff
from app.router import appointment
from app.router import auth

from app.model import doctor as doctor_model
from app.model import patient as patient_model
from app.model import medical_record as medical_record_model
from app.model import staff as staff_model
from app.model import appointment as appointment_model

from fastapi.responses import JSONResponse

from app.util.exceptions import PatientNotFoundException

from app.util.config import settings

from app.util.database import engine, Base


#Base.metadata.create_all(bind=engine)  

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION)

@app.exception_handler(PatientNotFoundException)
async def patient_not_found_handler(
    request: Request,
    exc: PatientNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Patient not found"
        } 
    ) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    print(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time

    print(f"Response: {response.status_code}")
    print(f"Time taken: {process_time:.4f} seconds")

    return response 

app.include_router(patient.router)
app.include_router(medical_record.router)
app.include_router(doctor.router)
app.include_router(staff.router)
app.include_router(appointment.router)
app.include_router(auth.router)


@app.get("/")
def hello():
    return {
        "message": "PATIENT MANAGEMENT SYSTEM API"
    }


@app.get("/about")
def about():
    return {
        "message": "FULLY FUNCTIONAL API TO MANAGE PATIENT RECORDS"
    }   