from datetime import datetime

from app.models import Appointment


def test_appointment_model():
    appointment = Appointment(
        patient_name="Jane Smith",
        doctor_id=2,
        start_time=datetime(2024, 1, 1, 14, 0),
        end_time=datetime(2024, 1, 1, 15, 0),
    )
    assert appointment.patient_name == "Jane Smith"
    assert appointment.doctor_id == 2
