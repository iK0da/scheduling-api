from fastapi import APIRouter, HTTPException
from datetime import datetime
from .models import AppointmentRequest
from .db import appointments_collection

router = APIRouter()

@router.get("/disponivel")
def get_avaliable_dates():
    return {"msg": "em breve"}

@router.post("/marcar/{year}/{month}/{day}/{hour}/{minutes}")
def create_appointment(year:int,month:int,day:int,hour:int,minutes:int, data:AppointmentRequest):
    date = datetime(year, month, day, hour, minutes)
    if appointments_collection.find_one({"datetime": date}):
        raise HTTPException(status_code=400, detail="Horário já marcado.")
    appointments_collection.insert_one({
        "datetime":date,
        "service": data.service,
        "client_name": data.client_name
    })
    return {"msg": "Agendamento confirmado"}

@router.get("/agenda/{year}/{month}")
def get_month_agenda(year: int, month: int):
    from calendar import monthrange

    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, monthrange(year, month)[1], 23, 59)

    appointments = appointments_collection.find({
        "datetime": {"$gte": first_day, "$lte": last_day}
    }).sort("datetime", 1)

    agenda = {}

    for appt in appointments:
        dt = appt["datetime"]
        day_str = dt.strftime("%Y-%m-%d")
        entry = {
            "horario": dt.strftime("%H:%M"),
            "service": appt["service"],
            "client_name": appt["client_name"]
        }

        if day_str not in agenda:
            agenda[day_str] = []
        agenda[day_str].append(entry)

    return agenda
