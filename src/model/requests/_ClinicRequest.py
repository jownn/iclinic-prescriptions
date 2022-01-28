from pydantic import BaseModel


class ClinicRequest(BaseModel):
    id: int
