FROM python:3.12-slim  

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN groupadd -r app && useradd -r -g app app \
    && chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

ENV PYTHONUTF8=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8