from pydantic import BaseModel


class PatientResponse(BaseModel):
    id: int
