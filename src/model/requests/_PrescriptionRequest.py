from typing import Optional

from pydantic import BaseModel

from src.model.requests import ClinicRequest, PhysicianRequest, PatientRequest


class PrescriptionRequest(BaseModel):
    clinic: ClinicRequest
    physician: PhysicianRequest
    patient: PatientRequest
    text: str

    class Config:
        orm_mode = True
