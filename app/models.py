from pydantic import BaseModel
from typing import Literal

class AppointmentRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    service: Literal["extensão", "manutenção", "remoção"]
    client_name: str