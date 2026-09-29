from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.util.database import Base


class MedicalRecord(Base):

    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(String,ForeignKey("patients.id"))
    doctor_id = Column(String,ForeignKey("doctors.id")) 

    diagnosis = Column(String)
    treatment = Column(String)

    patient = relationship( "Patient", back_populates="records")  
    doctor = relationship( "Doctor",back_populates="records")  