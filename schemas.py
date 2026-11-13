
from pydantic import BaseModel, Field


class ClinicalDataCreate(BaseModel):
    patient_name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    diagnosis: str = Field(min_length=1)
    treatment: str = Field(min_length=1)

    # Three additional patient data fields
    blood_type: str = Field(min_length=1)
    allergies: str = Field(min_length=1)
    emergency_contact: str = Field(min_length=1)


class ClinicalDataResponse(ClinicalDataCreate):
    id: int
