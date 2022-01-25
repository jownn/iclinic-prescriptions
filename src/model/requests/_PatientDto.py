from pydantic import BaseModel


class PatientDto(BaseModel):
    id: int
