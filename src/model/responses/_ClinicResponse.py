from pydantic import BaseModel


class ClinicResponse(BaseModel):
    id: int
