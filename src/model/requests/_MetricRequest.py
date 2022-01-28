from typing import Optional

from pydantic import BaseModel


class MetricRequest(BaseModel):
    clinic_id: Optional[int]
    clinic_name: Optional[str]
    physician_id: int
    physician_name: str
    physician_crm: str
    patient_id: int
    patient_name: str
    patient_email: str
    patient_phone: str
    prescription_id: int
