from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.util.database import Base


class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(String, primary_key=True, index=True)

    name = Column(String)
    email = Column(String)
    phone = Column(String)
    specialization = Column(String)
    department = Column(String)
    experience = Column(Integer)

    records = relationship(
        "MedicalRecord",
        back_populates="doctor"
    ) 
    appointments = relationship(
    "Appointment",
    back_populates="doctor"
)