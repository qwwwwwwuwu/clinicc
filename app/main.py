import os
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL')}")
import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/appointments/", response_model=schemas.AppointmentRead)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    """
    Создание новой записи на приём.
    Проверяет уникальность пары doctor_id + start_time.
    """
    # Проверка существующей записи врача на это время
    existing = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == appointment.doctor_id,
            models.Appointment.start_time == appointment.start_time,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="Doctor already has an appointment at this time"
        )

    return crud.create_appointment(db, appointment)


@app.get("/appointments/{appointment_id}", response_model=schemas.AppointmentRead)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Получение записи по ID.
    Возвращает 404 если запись не найдена.
    """
    db_appointment = crud.get_appointment(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@app.get("/health")
def health_check():
    """Эндпоинт для проверки работоспособности сервиса"""
    return {"status": "ok"}
