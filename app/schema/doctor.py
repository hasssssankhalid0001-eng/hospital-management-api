from pydantic import BaseModel,field_validator
from typing import Optional


class DoctorCreate(BaseModel):
    id: str 
    name: str
    specialization: str
    department: str
    experience: int
    email: str
    phone:str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if len(value) != 10 or not value.isdigit():

            raise ValueError("Phone number must contain exactly 10 digits")

        return value


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    department: Optional[str] = None
    experience: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("phone")

    @classmethod

    def validate_phone(cls, value):

        if value is not None and (len(value) != 10 or not value.isdigit()):

            raise ValueError("Phone number must contain exactly 10 digits")

        return value
    