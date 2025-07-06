#-*- coding: utf-8 -*-

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_appointment():
    response=client.post(
      "/appointments/",
      json={
          "patient_name": "John Doe",

          "doctor_id":1,
          "start_time": "2024-01-01T11:00:00",
          "end_time":"2024-01-01T12:00:00",
      },  
    )

    assert response.status_code==200
    appointment_id=response=response.json()["id"]

    response=client.get("/appontments/{appointment_id}")
    assert response.status_code ==200
    assert response.json()["patient_name"]=="John Doe"