from pydantic import BaseModel
from typing import Literal

class AppointmentRequest(BaseModel):
    service: Literal["extensão", "manutenção", "remoção"]
    client_name: str