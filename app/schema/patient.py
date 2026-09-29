from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    
    Pid:Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')] 
    city: Annotated[str, Field(..., description='City where the patient is living')] 
    age:Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')] 
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description= 'Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    phone: str
    email: str 

    @field_validator("phone")
    @classmethod

    def validate_phone(cls, value):

        if len(value) != 10 or not value.isdigit():

            raise ValueError("Phone number must contain exactly 10 digits")

        return value

    @computed_field 
    @property
    def bmi(self) -> float:
        bmi = round(self. weight/(self.height**2),2)
        return bmi

    @computed_field 
    @property
    def verdict (self) -> str: 

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'overweight'
        else: 
            return 'Obese'

class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female","others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)] 
    phone: Optional[str]
    email: Optional[str]

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if len(value) != 10 or not value.isdigit():

            raise ValueError("Phone number must contain exactly 10 digits")

        return value
        
#RESPONSE MODEL 
class PatientResponse(BaseModel):
    Pid: str
    name: str
    city: str
    age: int
    gender: Literal['male', 'female', 'others']
    height: float
    weight: float
    bmi: float
    verdict: str
    phone: str
    email: str
