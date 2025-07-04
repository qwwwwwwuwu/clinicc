from datetime import datetime

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_id: int
    start_time: datetime
    end_time: datetime


class AppointmentRead(AppointmentCreate):
    id: int
