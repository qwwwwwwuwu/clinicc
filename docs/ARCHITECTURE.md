компоненты

[Client] → [FastAPI] → [SQLAlchemy] → [PostgreSQL]
           ↑        ↓
       [Pydantic]  [CRUD]

связь
1 FastAPI
   - Принимает HTTP-запросы
   - Валидирует данные через Pydantic
   - Вызывает CRUD-операции

2 Sqlachemy
   - ORM для работы с PostgreSQL
   - Реализует уникальное ограничение `(doctor_id + start_time)`

3 postgres
   - Хранит записи о приёмах
   - Обеспечивает транзакционность