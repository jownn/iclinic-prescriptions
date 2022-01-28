from typing import Optional

from pydantic import BaseModel


class MetricResponse(BaseModel):
    id: str
