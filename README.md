что есть
1 Образ non-root и все секреты через env
2 CRUD работает, уникальность соблюдена
3 Все тесты проходят локально и в CI
4 Код без ошибок black/isort/flake8
5 Структура проекта понятна
6 Цели Makefile выполняются
7 HEALTHCHECK корректен
8 Понятный ридми (уже на ваше усмотрение)
9 После тестов CI собирает и пушит Docker-образ.
10 Расширенный Makefile: команды make up, make down, make migrate и т. д.

Микросервис для записи пациентов к врачам.


```bash
git clone https://github.com/qwwwwwwuwu/clinic.git
cd clinic-appointments
cp .env.example .env  # редактируйте при необходимости
make run
```


- `POST /appointments/` - Создать запись
  ```json
  {
    "patient_name": "John Doe",
    "doctor_id": 1,
    "start_time": "2024-01-01T10:00:00",
    "end_time": "2024-01-01T11:00:00"
  }
  ```
- `GET /appointments/{id}` - Получить запись
- `GET /health` - Проверка здоровья сервиса


```bash
make test  # запуск тестов
make lint  # проверка стиля кода
```


После запуска откройте в браузере:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc


```bash
make stop  # останавливает контейнеры
make clean # полная очистка
```

