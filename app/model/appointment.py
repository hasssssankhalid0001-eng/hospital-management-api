from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.util.database import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        String,
        ForeignKey("patients.id")
    )

    doctor_id = Column(
        String,
        ForeignKey("doctors.id")
    )

    appointment_date = Column(String)

    reason = Column(String)
    status = Column(String)

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )