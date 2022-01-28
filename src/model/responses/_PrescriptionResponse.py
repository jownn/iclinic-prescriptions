from typing import Optional

from pydantic import BaseModel

from src.model.responses import ClinicResponse, PhysicianResponse, PatientResponse, MetricResponse


class PrescriptionResponse(BaseModel):
    clinic: ClinicResponse
    physician: PhysicianResponse
    patient: PatientResponse
    text: str
    metric: MetricResponse

    class Config:
        orm_mode = True
