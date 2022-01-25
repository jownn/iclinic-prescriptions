from typing import Optional

from pydantic import BaseModel

from src.model.requests import ClinicDto, PhysicianDto, PatientDto, MetricDto


class PrescriptionDto(BaseModel):
    clinic: ClinicDto
    physician: PhysicianDto
    patient: PatientDto
    text: str
    metric: Optional[MetricDto]

    class Config:
        orm_mode = True