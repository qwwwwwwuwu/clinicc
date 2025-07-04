сущности

APPOINTMENT (
  id: INTEGER (PK)
  patient_name: TEXT
  doctor_id: INTEGER
  start_time: TIMESTAMP
  end_time: TIMESTAMP
)

ограничения
- `UNIQUE(doctor_id, start_time)`
- `start_time < end_time` (проверка на уровне приложения)