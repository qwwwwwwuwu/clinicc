from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from .database import Base


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", name="unique_doctor_time"),
    )
