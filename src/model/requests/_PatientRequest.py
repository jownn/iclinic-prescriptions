from pydantic import BaseModel


class PatientRequest(BaseModel):
    id: int
