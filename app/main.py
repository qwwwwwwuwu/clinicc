from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# Создание таблиц
models.Base.metadata.create_all(bind=engine)  # type: ignore[attr-defined]

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/appointments/", response_model=schemas.AppointmentRead)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
) -> schemas.AppointmentRead:
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

    db_appointment = crud.create_appointment(db, appointment)
    return schemas.AppointmentRead.from_orm(
        db_appointment
    )  # Преобразование модели в схему


@app.get("/appointments/{appointment_id}", response_model=schemas.AppointmentRead)
def read_appointment(
    appointment_id: int, db: Session = Depends(get_db)
) -> schemas.AppointmentRead:
    db_appointment = crud.get_appointment(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return schemas.AppointmentRead.from_orm(db_appointment)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
