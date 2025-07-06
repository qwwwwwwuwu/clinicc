# Используем минимальный официальный образ Python
FROM python:3.12-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём пользователя с пониженными правами безопасности
RUN groupadd -r app && useradd -r -g app app \
    && chown -R app:app /app
USER app

# Добавляем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# HEALTHCHECK для FastAPI
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Команда по умолчанию (только для "api" сервиса)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
