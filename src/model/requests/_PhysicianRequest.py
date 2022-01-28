from pydantic import BaseModel


class PhysicianRequest(BaseModel):
    id: int
