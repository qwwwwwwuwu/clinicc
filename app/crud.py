from typing import Optional

from sqlalchemy.orm import Session

from . import models


def create_appointment(db: Session, appointment) -> models.Appointment:
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)  # type: ignore[arg-type]
        .first()
    )
