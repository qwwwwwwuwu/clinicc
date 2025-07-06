import os
import sys
from typing import cast
from urllib.parse import quote_plus, urlparse

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_database_config() -> tuple[str, str, str, str, str]:
    """Получение конфигурации БД с проверкой типов."""
    if "pytest" in sys.modules:
        return ("test", "test", "test", "localhost", "5432")

    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        parsed = urlparse(DATABASE_URL)
        return (
            cast(str, parsed.username),
            cast(str, parsed.password),
            cast(str, parsed.path[1:]),  # удаляем "/"
            cast(str, parsed.hostname),
            str(parsed.port) if parsed.port else "5432",
        )

    DB_USER = cast(str, os.getenv("DB_USER")) or "test"
    DB_PASSWORD = cast(str, os.getenv("DB_PASSWORD")) or "test"
    DB_NAME = cast(str, os.getenv("DB_NAME")) or "test"
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Не заданы обязательные переменные окружения для базы данных")

    return (
        cast(str, DB_USER),
        cast(str, DB_PASSWORD),
        cast(str, DB_NAME),
        cast(str, DB_HOST),
        cast(str, DB_PORT),
    )


DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT = get_database_config()

# Кодирование пароля (на случай спецсимволов)
encoded_password = quote_plus(DB_PASSWORD)

# Окончательный DSN
final_db_url: str = (
    f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    if "pytest" not in sys.modules and not os.getenv("DATABASE_URL")
    else f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(final_db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Логируем DSN (без пароля) — только вне pytest
if __name__ == "__main__" or "pytest" not in sys.modules:
    safe_dsn = final_db_url.replace(DB_PASSWORD, "***")
    print(f"[DB] Используется DSN: {safe_dsn}")
