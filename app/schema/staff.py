from pydantic import BaseModel,field_validator
from typing import Optional


class StaffCreate(BaseModel):
    id: str
    name: str
    role: str
    department: str
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if len(value) != 10 or not value.isdigit():

            raise ValueError("Phone number must contain exactly 10 digits")

        return value

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None  

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if len(value) != 10 or not value.isdigit():

            raise ValueError("Phone number must contain exactly 10 digits")

        return value  