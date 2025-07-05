from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

# Решение для обхода проверки mypy
try:
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        pass

except ImportError:
    Base = declarative_base()  # type: ignore[misc, assignment]


class Appointment(Base):  # type: ignore[misc]
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", name="unique_doctor_time"),
    )
