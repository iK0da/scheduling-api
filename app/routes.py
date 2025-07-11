from fastapi import APIRouter, HTTPException
from datetime import datetime
from .models import AppointmentRequest
from .db import appointments_collection

router = APIRouter()

@router.get("/disponivel")
def get_avaliable_dates():
    return {"msg": "em breve"}

@router.post("/marcar/{year}{month}{day}{hour}{minute}")
def create_appointment(year:int,month:int,day:int,hour:int,minutes:int, data:AppointmentRequest = None):
    date = datetime(year, month, day, hour, minute)
    if appointments_collection.find_one({"datetime": date}):
        raise HTTPException(status_code=400, detail="Horário já marcado.")
    appointments_collection.insert_one({
        "datetime":date,
        "service": data.service,
        "client_name": data.client_name
    })
    return {"msg": "Agendamento confirmado"}

@router.get("/agenda/{year}{month}")
def get_month_overview(year:int,month:int):
    return {"msg":"em breve"}