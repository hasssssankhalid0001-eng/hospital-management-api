from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.util.database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)
    phone = Column(String)
    email = Column(String)  
    
    records = relationship("MedicalRecord",back_populates="patient") 
    appointments = relationship("Appointment",back_populates="patient") 